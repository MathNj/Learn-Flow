#!/usr/bin/env python3
"""
Generate MCP wrapper scripts from templates.

Generates Python, Bash, or JavaScript wrapper scripts that follow
the MCP code execution pattern for token efficiency.

Generated scripts process data outside agent context and return
minimal results, achieving 80-99% token savings.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import jinja2
except ImportError:
    print(json.dumps({
        "status": "error",
        "message": "jinja2 is required. Install with: pip install jinja2"
    }), file=sys.stderr)
    sys.exit(1)


# Default configuration
DEFAULT_LANGUAGES = ["python", "bash", "javascript"]
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def load_template(language: str) -> jinja2.Template:
    """Load a wrapper template for the given language."""
    template_file = TEMPLATE_DIR / f"{language}_wrapper.{language if language != 'javascript' else 'js'}.jinja2"

    if not template_file.exists():
        raise ValueError(f"Template not found for language: {language}")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    return env.get_template(template_file.name)


def generate_wrapper(
    mcp_server: str,
    tool: str,
    language: str,
    description: Optional[str] = None,
    tool_args: Optional[List[Dict[str, Any]]] = None,
    limit: int = 10,
    output: Optional[Path] = None,
    use_mcp_client: bool = False,
    allow_eval: bool = False,
    dry_run: bool = False
) -> str:
    """
    Generate a wrapper script.

    Args:
        mcp_server: Name of the MCP server
        tool: Name of the tool
        language: Programming language (python, bash, javascript)
        description: Script description
        tool_args: List of tool argument definitions
        limit: Default result limit
        output: Output file path
        use_mcp_client: Include MCP client imports
        allow_eval: Allow eval in filter expressions
        dry_run: Print instead of write

    Returns:
        Generated script content
    """
    if language not in DEFAULT_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}. Choose from: {DEFAULT_LANGUAGES}")

    # Default description
    if not description:
        description = f"Wrapper for {mcp_server} {tool}"

    # Default tool args
    if tool_args is None:
        tool_args = []

    # Normalize tool args
    normalized_args = []
    for arg in tool_args:
        if isinstance(arg, str):
            normalized_args.append({
                "name": arg,
                "param_name": arg,
                "required": False,
                "help": f"{arg} parameter",
                "default": None
            })
        elif isinstance(arg, dict):
            normalized_args.append({
                "name": arg.get("name", arg.get("param_name", "arg")),
                "param_name": arg.get("param_name", arg.get("name", "arg")),
                "required": arg.get("required", False),
                "help": arg.get("help", f"Parameter {arg.get('name', 'arg')}"),
                "default": arg.get("default")
            })

    # Load and render template
    template = load_template(language)

    # Language-specific settings
    use_mcp_sdk = use_mcp_client and language == "javascript"

    content = template.render(
        description=description,
        mcp_server=mcp_server,
        tool=tool,
        tool_args=normalized_args,
        limit=limit,
        use_mcp_client=use_mcp_client,
        use_mcp_sdk=use_mcp_sdk,
        allow_eval=allow_eval
    )

    return content


def write_wrapper(content: str, output: Path, language: str, dry_run: bool = False) -> None:
    """Write wrapper script to file."""
    # Determine output path
    if output is None:
        output = Path(f"wrapper.{language if language != 'javascript' else 'js'}" if language != 'bash' else 'wrapper.sh')

    # Ensure parent directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"Would write to: {output}")
        print("---")
        print(content)
        return

    # Write file
    with open(output, 'w') as f:
        f.write(content)

    # Make executable
    os.chmod(output, 0o755)

    print(json.dumps({
        "status": "success",
        "message": f"Generated wrapper: {output}",
        "output": str(output),
        "language": language
    }))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate MCP wrapper scripts following the code execution pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Python wrapper
  %(prog)s --mcp-server sheets-mcp --tool getSheet --language python

  # Generate with custom args
  %(prog)s --server sheets-mcp --tool getSheet --language python \\
          --tool-arg sheet_id --tool-arg range --output scripts/sheet_wrapper.py

  # Generate Bash wrapper with filter
  %(prog)s --server k8s-mcp --tool getPods --language bash \\
          --filter 'status=="Running"' --limit 5

  # Dry run (print to stdout)
  %(prog)s --server sheets-mcp --tool getSheet --language python --dry-run
        """
    )

    # Required arguments
    parser.add_argument(
        "--mcp-server", "--server",
        required=True,
        help="MCP server name"
    )
    parser.add_argument(
        "--tool",
        required=True,
        help="MCP tool name"
    )

    # Wrapper configuration
    parser.add_argument(
        "--language", "--lang",
        choices=DEFAULT_LANGUAGES,
        default="python",
        help="Wrapper language (default: python)"
    )
    parser.add_argument(
        "--description", "--desc",
        help="Wrapper description"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Default result limit (default: 10)"
    )

    # Tool arguments
    parser.add_argument(
        "--tool-arg",
        action="append",
        dest="tool_args",
        help="Tool argument (can be specified multiple times). "
             "Format: name or name:param_name or JSON for full config"
    )

    # Output options
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout instead of writing file"
    )

    # Advanced options
    parser.add_argument(
        "--use-mcp-client",
        action="store_true",
        help="Include MCP client imports in generated script"
    )
    parser.add_argument(
        "--allow-eval",
        action="store_true",
        help="Allow eval in filter expressions (use with caution)"
    )

    args = parser.parse_args()

    # Parse tool arguments
    parsed_tool_args = []
    if args.tool_args:
        for arg in args.tool_args:
            if arg.startswith("{"):
                # JSON format
                try:
                    parsed_tool_args.append(json.loads(arg))
                except json.JSONDecodeError as e:
                    print(json.dumps({
                        "status": "error",
                        "message": f"Invalid JSON in tool-arg: {e}"
                    }), file=sys.stderr)
                    sys.exit(2)
            elif ":" in arg:
                # name:param_name format
                name, param_name = arg.split(":", 1)
                parsed_tool_args.append({
                    "name": name,
                    "param_name": param_name,
                    "required": False,
                    "help": f"{name} parameter"
                })
            else:
                # Simple name
                parsed_tool_args.append(arg)

    try:
        # Generate wrapper
        content = generate_wrapper(
            mcp_server=args.mcp_server,
            tool=args.tool,
            language=args.language,
            description=args.description,
            tool_args=parsed_tool_args,
            limit=args.limit,
            output=args.output,
            use_mcp_client=args.use_mcp_client,
            allow_eval=args.allow_eval,
            dry_run=args.dry_run
        )

        # Write or print
        if args.dry_run:
            write_wrapper(content, args.output or Path("wrapper.txt"), args.language, dry_run=True)
        else:
            write_wrapper(content, args.output, args.language, dry_run=False)

        sys.exit(0)

    except ValueError as e:
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "error_type": "ValueError"
        }), file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
