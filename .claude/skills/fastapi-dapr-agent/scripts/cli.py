"""
CLI argument parser for FastAPI Dapr Agent (US0-T003).

Parses command-line arguments and validates them against config models.
"""
import argparse
import sys
from typing import List, Optional

try:
    from .config import ServiceType, FeatureFlag, ServiceConfig
except ImportError:
    from config import ServiceType, FeatureFlag, ServiceConfig


SERVICE_TYPE_CHOICES = [t.value for t in ServiceType]
FEATURE_CHOICES = [f.value for f in FeatureFlag]


def parse_features(features_str: Optional[str]) -> List[FeatureFlag]:
    """Parse comma-separated feature string into list of FeatureFlags."""
    if not features_str:
        return [FeatureFlag.HEALTH]

    feature_list = []
    for f in features_str.split(","):
        f = f.strip()
        try:
            feature = FeatureFlag(f)
            feature_list.append(feature)
        except ValueError:
            print(f"Error: Invalid feature '{f}'. Valid options: {', '.join(FEATURE_CHOICES)}")
            sys.exit(4)

    # Always include health
    if FeatureFlag.HEALTH not in feature_list:
        feature_list.append(FeatureFlag.HEALTH)

    return feature_list


def parse_topics(topics_str: Optional[str]) -> List[dict]:
    """
    Parse comma-separated topic string into list of topic configs.

    Format: name:subscribe:publish
    Example: learning.query:true:false,learning.routed:false:true
    """
    if not topics_str:
        return []

    topics = []
    for t in topics_str.split(","):
        t = t.strip()
        parts = t.split(":")
        if len(parts) != 3:
            print(f"Error: Invalid topic format '{t}'. Expected: name:subscribe:publish")
            sys.exit(4)

        name, subscribe_str, publish_str = parts
        try:
            subscribe = subscribe_str.strip().lower() in ("true", "1", "yes")
            publish = publish_str.strip().lower() in ("true", "1", "yes")

            if not subscribe and not publish:
                print(f"Error: Topic '{name}' must have at least subscribe or publish enabled")
                sys.exit(4)

            topics.append({
                "name": name.strip(),
                "subscribe": subscribe,
                "publish": publish,
                "event_type": name.strip().replace(".", "_").replace("-", "_") + "Event",
            })
        except Exception as e:
            print(f"Error parsing topic '{t}': {e}")
            sys.exit(4)

    return topics


def parse_invoke_targets(targets_str: Optional[str]) -> List[str]:
    """Parse comma-separated invoke targets string."""
    if not targets_str:
        return []

    return [t.strip() for t in targets_str.split(",") if t.strip()]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="generate_service",
        description="Generate FastAPI microservices with Dapr sidecar integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate a triage service:
    %(prog)s --service-name triage-service --service-type triage

  Generate a concepts service with agent:
    %(prog)s -n concepts-service -t concepts -d "Explains Python concepts"

  Generate with custom features:
    %(prog)s -n my-service -t generic -f pubsub,state,invocation

  Generate with custom topics:
    %(prog)s -n my-service -t generic --topics "my.topic:true:false,other.topic:false:true"

  Dry run (show what would be generated):
    %(prog)s -n test-service --dry-run --verbose
        """
    )

    # Required arguments
    parser.add_argument(
        "--service-name", "-n",
        required=True,
        help="Name of the service (kebab-case, e.g., 'my-service')"
    )

    # Optional arguments
    parser.add_argument(
        "--service-type", "-t",
        choices=SERVICE_TYPE_CHOICES,
        default=ServiceType.GENERIC.value,
        help="Type of microservice (default: generic)"
    )

    parser.add_argument(
        "--description", "-d",
        default="",
        help="Service description for documentation"
    )

    parser.add_argument(
        "--output-dir", "-o",
        default="./generated",
        help="Output directory for generated service (default: ./generated)"
    )

    parser.add_argument(
        "--features", "-f",
        default="",
        help=f"Comma-separated features: {', '.join(FEATURE_CHOICES)} (default: health)"
    )

    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Application port (default: 8000)"
    )

    parser.add_argument(
        "--python-version",
        default="3.11",
        help="Python version (default: 3.11)"
    )

    parser.add_argument(
        "--openai-model",
        default=None,
        help='OpenAI model for agent services (default: "gpt-4")'
    )

    parser.add_argument(
        "--topics",
        default=None,
        help='Comma-separated topics (format: name:subscribe:publish, e.g., "topic1:true:false")'
    )

    parser.add_argument(
        "--invoke-targets",
        default=None,
        help='Comma-separated target services for invocation (e.g., "service1,service2")'
    )

    parser.add_argument(
        "--version",
        default="0.1.0",
        help="Initial version (default: 0.1.0)"
    )

    # Flags
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed progress"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output directory"
    )

    return parser.parse_args(argv)


def validate_service_name(name: str) -> tuple[bool, str]:
    """
    Validate service name is kebab-case.

    Returns:
        (is_valid, error_message)
    """
    import re

    if not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", name):
        return (
            False,
            "Service name must be kebab-case (lowercase letters, numbers, hyphens only, "
            "must start and end with alphanumeric)"
        )
    return True, ""


def build_config_from_args(args: argparse.Namespace) -> ServiceConfig:
    """
    Build ServiceConfig from parsed CLI arguments.

    Args:
        args: Parsed arguments from parse_args()

    Returns:
        ServiceConfig instance

    Raises:
        SystemExit: If configuration is invalid (exit code 2-4)
    """
    # Validate service name
    is_valid, error_msg = validate_service_name(args.service_name)
    if not is_valid:
        print(f"Error: {error_msg}")
        sys.exit(2)

    # Parse features
    features = parse_features(args.features)

    # Parse service type
    service_type = ServiceType(args.service_type)

    # Build config
    try:
        config_dict = {
            "service_name": args.service_name,
            "service_type": service_type,
            "description": args.description or f"{args.service_name.replace('-', ' ').title()} microservice",
            "version": args.version,
            "python_version": args.python_version,
            "port": args.port,
            "features": features,
        }

        # Add OpenAI model if agent feature or explicitly provided
        if FeatureFlag.AGENT in features or args.openai_model:
            config_dict["openai_model"] = args.openai_model or "gpt-4"

        config = ServiceConfig(**config_dict)

    except Exception as e:
        print(f"Error: Invalid configuration: {e}")
        sys.exit(4)

    return config


def main(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Main CLI entry point.

    Parses arguments and returns configuration for generation.

    Args:
        argv: Argument list (defaults to sys.argv[1:])

    Returns:
        Namespace with parsed args and config
    """
    args = parse_args(argv)

    # Build and validate config
    config = build_config_from_args(args)

    # Store config on args for easy access
    args.config = config

    return args


if __name__ == "__main__":
    args = main()
    if args.verbose:
        print(f"Service: {args.config.service_name}")
        print(f"Type: {args.config.service_type}")
        print(f"Features: {[f.value for f in args.config.features]}")
        print(f"Output: {args.output_dir}")
