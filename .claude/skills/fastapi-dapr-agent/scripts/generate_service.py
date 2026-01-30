#!/usr/bin/env python3
"""
Main generator script for FastAPI Dapr Agent (US0-T004).

Generates complete FastAPI microservices with Dapr sidecar integration.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Error: jinja2 is required. Install with: pip install jinja2")
    sys.exit(6)

try:
    from cli import parse_args, build_config_from_args
    from config import ServiceType, FeatureFlag, get_service_config, SERVICE_TYPE_CONFIGS
except ImportError:
    from scripts.cli import parse_args, build_config_from_args
    from scripts.config import ServiceType, FeatureFlag, get_service_config, SERVICE_TYPE_CONFIGS


# Exit codes per generator-interface.md
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_INVALID_SERVICE_NAME = 2
EXIT_INVALID_SERVICE_TYPE = 3
EXIT_INVALID_FEATURE_COMBO = 4
EXIT_OUTPUT_DIR_EXISTS = 5
EXIT_MISSING_DEPENDENCIES = 6
EXIT_TEMPLATE_ERROR = 7
EXIT_WRITE_PERMISSION = 8


class GeneratorError(Exception):
    """Base exception for generator errors."""
    def __init__(self, message: str, exit_code: int = EXIT_GENERAL_ERROR):
        self.message = message
        self.exit_code = exit_code
        super().__init__(message)


class ServiceGenerator:
    """Generates FastAPI microservice with Dapr integration."""

    def __init__(self, config, output_dir: Path, dry_run: bool = False, verbose: bool = False):
        """
        Initialize generator.

        Args:
            config: ServiceConfig instance
            output_dir: Output directory path
            dry_run: If True, show what would be generated without writing
            verbose: If True, print detailed progress
        """
        self.config = config
        self.output_dir = Path(output_dir) / config.service_name
        self.dry_run = dry_run
        self.verbose = verbose

        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Track generated files for cleanup on error
        self.generated_files: List[Path] = []

    def log(self, message: str, force: bool = False):
        """Print message if verbose or forced."""
        if self.verbose or force:
            print(message)

    def validate_output_dir(self):
        """Validate output directory doesn't exist or is empty."""
        if self.output_dir.exists():
            if not self.dry_run:
                # Check if directory is empty
                if any(self.output_dir.iterdir()):
                    raise GeneratorError(
                        f"Output directory '{self.output_dir}' exists and is not empty. "
                        "Use --force to overwrite.",
                        EXIT_OUTPUT_DIR_EXISTS
                    )

    def create_output_dir(self):
        """Create output directory if not exists."""
        if not self.dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_template(self, template_name: str, context: Dict) -> str:
        """
        Render a Jinja2 template.

        Args:
            template_name: Name of template file
            context: Template context variables

        Returns:
            Rendered template content
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise GeneratorError(
                f"Template error in '{template_name}': {e}",
                EXIT_TEMPLATE_ERROR
            )

    def write_file(self, relative_path: str, content: str):
        """
        Write content to file (unless dry-run).

        Args:
            relative_path: Relative path from output directory
            content: File content
        """
        file_path = self.output_dir / relative_path

        if self.dry_run:
            self.log(f"  Would create: {relative_path}")
            return

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        try:
            file_path.write_text(content)
            self.generated_files.append(file_path)
            self.log(f"  Created: {relative_path}")
        except PermissionError:
            raise GeneratorError(
                f"Write permission denied for '{file_path}'",
                EXIT_WRITE_PERMISSION
            )

    def cleanup(self):
        """Remove generated files on error."""
        for file_path in self.generated_files:
            try:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    # Remove empty directories
                    try:
                        file_path.rmdir()
                    except OSError:
                        pass  # Directory not empty, leave it
            except Exception:
                pass  # Best effort cleanup

    def get_template_context(self) -> Dict:
        """Get template context from config."""
        service_type = self.config.service_type
        type_config = SERVICE_TYPE_CONFIGS.get(service_type, SERVICE_TYPE_CONFIGS[ServiceType.GENERIC])

        return {
            "service_name": self.config.service_name,
            "service_title": self.config.service_name.replace("-", " ").title(),
            "service_type": service_type.value,
            "description": self.config.description,
            "version": self.config.version,
            "python_version": self.config.python_version,
            "port": self.config.port,
            "features": [f.value for f in self.config.features],
            "has_pubsub": FeatureFlag.PUBSUB in self.config.features,
            "has_state": FeatureFlag.STATE in self.config.features,
            "has_invocation": FeatureFlag.INVOCATION in self.config.features,
            "has_agent": FeatureFlag.AGENT in self.config.features,
            "has_health": FeatureFlag.HEALTH in self.config.features,
            "openai_model": self.config.openai_model or "gpt-4",
            "topics": type_config.get("topics", []),
            "invoke_targets": type_config.get("invoke_targets", []),
            "state_ttl": type_config.get("state_ttl"),
        }

    def generate(self):
        """Generate the complete service."""
        print(f"\n=== FastAPI Dapr Service Generator ===\n")
        print(f"Service: {self.config.service_name}")
        print(f"Type: {self.config.service_type.value}")
        print(f"Output: {self.output_dir}")
        print()

        # Validate output directory
        self.validate_output_dir()

        # Get template context
        context = self.get_template_context()

        # Count steps for progress reporting
        steps = [
            ("Creating project structure", self._create_project_structure),
            ("Generating FastAPI application", self._generate_fastapi_app),
            ("Adding configuration and logging", self._generate_config_logging),
            ("Generating API models", self._generate_models),
            ("Generating health endpoints", self._generate_health_endpoints),
        ]

        if FeatureFlag.PUBSUB in self.config.features:
            steps.append(("Adding Dapr pub/sub components", self._generate_pubsub))
        if FeatureFlag.STATE in self.config.features:
            steps.append(("Adding Dapr state management", self._generate_state))
        if FeatureFlag.INVOCATION in self.config.features:
            steps.append(("Adding service invocation", self._generate_invocation))
        if FeatureFlag.AGENT in self.config.features:
            steps.append(("Adding OpenAI agent integration", self._generate_agent))

        steps.extend([
            ("Generating Dockerfile", self._generate_dockerfile),
            ("Generating Kubernetes manifests", self._generate_k8s_manifests),
            ("Generating project files", self._generate_project_files),
        ])

        # Execute generation steps
        try:
            for i, (step_name, step_func) in enumerate(steps, 1):
                print(f"[{i}/{len(steps)}] {step_name}...")
                step_func(context)

            print()
            if self.dry_run:
                print("(dry-run mode - no files written)")
            else:
                print("Service generated successfully!")

            self._print_next_steps()

        except GeneratorError:
            self.cleanup()
            raise

    def _create_project_structure(self, context: Dict):
        """Create directory structure."""
        dirs = [
            "app",
            "app/api",
            "app/models",
            "app/services",
            "app/core",
            "tests",
            "k8s",
            "k8s/components",
        ]

        if FeatureFlag.AGENT in self.config.features:
            dirs.append("app/agents")

        for d in dirs:
            if not self.dry_run:
                (self.output_dir / d).mkdir(parents=True, exist_ok=True)
            self.log(f"  Created directory: {d}")

        # Create __init__.py files
        init_dirs = ["app", "app/api", "app/models", "app/services", "app/core", "tests"]
        if FeatureFlag.AGENT in self.config.features:
            init_dirs.append("app/agents")

        for d in init_dirs:
            self.write_file(f"{d}/__init__.py", "")

    def _generate_fastapi_app(self, context: Dict):
        """Generate main FastAPI application."""
        content = self.render_template("fastapi_app.py.jinja2", context)
        self.write_file("app/main.py", content)

    def _generate_config_logging(self, context: Dict):
        """Generate config and logging modules."""
        # Config
        content = self.render_template("core_config.py.jinja2", context)
        self.write_file("app/core/config.py", content)

        # Logging
        content = self.render_template("core_logging.py.jinja2", context)
        self.write_file("app/core/logging.py", content)

    def _generate_models(self, context: Dict):
        """Generate Pydantic models."""
        content = self.render_template("models_schemas.py.jinja2", context)
        self.write_file("app/models/schemas.py", content)

    def _generate_health_endpoints(self, context: Dict):
        """Generate health check endpoints."""
        content = self.render_template("health_routes.py.jinja2", context)
        self.write_file("app/api/health.py", content)

    def _generate_pubsub(self, context: Dict):
        """Generate pub/sub components."""
        # Subscriber mixin
        content = self.render_template("pubsub_mixin.py.jinja2", context)
        self.write_file("app/services/pubsub.py", content)

        # Publisher
        content = self.render_template("publisher_mixin.py.jinja2", context)
        self.write_file("app/services/publisher.py", content)

        # Event handlers
        content = self.render_template("event_handlers.py.jinja2", context)
        self.write_file("app/api/events.py", content)

    def _generate_state(self, context: Dict):
        """Generate state management."""
        content = self.render_template("state_mixin.py.jinja2", context)
        self.write_file("app/services/state.py", content)

    def _generate_invocation(self, context: Dict):
        """Generate service invocation."""
        content = self.render_template("invoke_mixin.py.jinja2", context)
        self.write_file("app/services/invoke.py", content)

    def _generate_agent(self, context: Dict):
        """Generate OpenAI agent integration."""
        content = self.render_template("agent_mixin.py.jinja2", context)
        self.write_file("app/agents/openai.py", content)

    def _generate_dockerfile(self, context: Dict):
        """Generate Dockerfile."""
        content = self.render_template("dockerfile.jinja2", context)
        self.write_file("Dockerfile", content)

    def _generate_k8s_manifests(self, context: Dict):
        """Generate Kubernetes manifests."""
        # Deployment
        content = self.render_template("k8s_deployment.yaml.jinja2", context)
        self.write_file("k8s/deployment.yaml", content)

        # Service
        content = self.render_template("k8s_service.yaml.jinja2", context)
        self.write_file("k8s/service.yaml", content)

        # ConfigMap
        content = self.render_template("k8s_configmap.yaml.jinja2", context)
        self.write_file("k8s/configmap.yaml", content)

        # HPA
        content = self.render_template("k8s_hpa.yaml.jinja2", context)
        self.write_file("k8s/hpa.yaml", content)

        # Dapr components
        if FeatureFlag.PUBSUB in self.config.features:
            content = self.render_template("k8s_components_pubsub.yaml.jinja2", context)
            self.write_file("k8s/components/pubsub.yaml", content)

        if FeatureFlag.STATE in self.config.features:
            content = self.render_template("k8s_components_statestore.yaml.jinja2", context)
            self.write_file("k8s/components/statestore.yaml", content)

    def _generate_project_files(self, context: Dict):
        """Generate project configuration files."""
        # pyproject.toml
        content = self.render_template("pyproject.toml.jinja2", context)
        self.write_file("pyproject.toml", content)

        # .env.example
        content = self.render_template("env.example.jinja2", context)
        self.write_file(".env.example", content)

        # .gitignore
        content = self.render_template("gitignore.jinja2", context)
        self.write_file(".gitignore", content)

        # docker-compose.yml
        content = self.render_template("docker-compose.yml.jinja2", context)
        self.write_file("docker-compose.yml", content)

        # README
        content = self.render_template("README.md.jinja2", context)
        self.write_file("README.md", content)

        # tests/conftest.py
        content = self.render_template("tests_conftest.py.jinja2", context)
        self.write_file("tests/conftest.py", content)

    def _print_next_steps(self):
        """Print next steps after generation."""
        print("\nNext steps:")
        print(f"  1. cd {self.output_dir}")
        print(f"  2. cp .env.example .env")
        print(f"  3. Edit .env with your configuration")
        print(f"  4. docker-compose up   # Local development")
        print(f"  5. kubectl apply -f k8s/  # Kubernetes deployment")
        print()
        print(f"Connection: http://localhost:{self.config.port}")
        print(f"Health: http://localhost:{self.config.port}/health")
        print(f"Docs: http://localhost:{self.config.port}/docs")


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()

        # Build config
        config = build_config_from_args(args)

        # Create generator
        generator = ServiceGenerator(
            config=config,
            output_dir=Path(args.output_dir),
            dry_run=args.dry_run,
            verbose=args.verbose,
        )

        # Generate service
        generator.generate()

        # Output JSON if requested (for programmatic use)
        if hasattr(args, 'output_json') and args.output_json:
            result = {
                "success": True,
                "service_name": config.service_name,
                "service_type": config.service_type.value,
                "output_dir": str(generator.output_dir),
                "features": [f.value for f in config.features],
            }
            print(json.dumps(result, indent=2))

        return EXIT_SUCCESS

    except GeneratorError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return e.exit_code
    except KeyboardInterrupt:
        print("\nGeneration cancelled.", file=sys.stderr)
        return EXIT_GENERAL_ERROR
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return EXIT_GENERAL_ERROR


if __name__ == "__main__":
    sys.exit(main())
