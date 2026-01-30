#!/usr/bin/env python3
"""
Demonstration of token savings from MCP code execution pattern.

Shows before/after token usage for common MCP operations.
"""

import argparse
import json
import sys
from typing import List

from token_utils import (
    SCENARIO_MEASUREMENTS,
    compare_scenarios,
    format_comparison,
    get_scenario_measurement
)


def print_table(scenarios: List[str]) -> None:
    """Print comparison table."""
    print("\n" + "=" * 80)
    print("Token Efficiency: Direct MCP Call vs Code Execution Pattern")
    print("=" * 80)
    print()
    print(f"{'Scenario':<30} {'Direct':>12} {'Pattern':>12} {'Savings':>12}")
    print("-" * 80)

    total_direct = 0
    total_pattern = 0

    for scenario in scenarios:
        measurement = get_scenario_measurement(scenario)

        direct_str = f"{measurement.direct_tokens:,}"
        pattern_str = f"{measurement.pattern_tokens:,}"
        savings_str = f"{measurement.savings_percent}%"

        print(f"{measurement.operation:<30} {direct_str:>12} {pattern_str:>12} {savings_str:>12}")

        total_direct += measurement.direct_tokens
        total_pattern += measurement.pattern_tokens

    print("-" * 80)
    total_savings = ((total_direct - total_pattern) / total_direct * 100) if total_direct > 0 else 0
    print(f"{'TOTAL':<30} {total_direct:>12,} {total_pattern:>12,} {total_savings:>11.1f}%")
    print()


def print_detailed_example(scenario: str) -> None:
    """Print detailed example for a scenario."""
    measurement = get_scenario_measurement(scenario)

    print("\n" + "=" * 80)
    print(f"Detailed Example: {measurement.operation}")
    print("=" * 80)
    print()

    # Direct MCP Call (Inefficient)
    print("Direct MCP Call (Inefficient):")
    print("-" * 40)
    print(f"  Operation: Get {measurement.data_size:,} items")
    print(f"  Token Cost: {measurement.direct_tokens:,} tokens")
    print("  How it works:")
    print("    1. Agent loads tool definitions (~15K tokens)")
    print("    2. MCP server returns ALL data into context")
    print("    3. Agent processes in context (more tokens!)")
    print("  Problem: Most data is never used")
    print()

    # Code Execution Pattern (Efficient)
    print("Code Execution Pattern (Efficient):")
    print("-" * 40)
    print(f"  Operation: Filter and return 5 items")
    print(f"  Token Cost: {measurement.pattern_tokens:,} tokens")
    print("  How it works:")
    print("    1. Agent calls script via Bash tool")
    print("    2. Script calls MCP server (outside context)")
    print("    3. Script filters/processes data")
    print("    4. Only results return to agent")
    print("  Solution: Only what you need enters context")
    print()

    # Token comparison
    savings = measurement.savings
    print(f"Token Savings: {savings:,} tokens ({measurement.savings_percent}%)")
    print(f"Efficiency: {measurement.direct_tokens // measurement.pattern_tokens}x reduction")
    print()


def print_json_output(scenarios: List[str]) -> None:
    """Print JSON formatted output."""
    comparison = compare_scenarios(scenarios)
    print(json.dumps(comparison, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Demonstrate token savings from MCP code execution pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show all scenarios
  %(prog)s

  # Show specific scenarios
  %(prog)s sheet-large k8s-pods

  # Detailed example
  %(prog)s --detail sheet-large

  # JSON output
  %(prog)s --json

Available scenarios:
  sheet-large   Google Sheets with 10,000 rows
  k8s-pods      Kubernetes 100 pods
  file-scan     Repository scan 1,000 files
  db-query      Database query 500 rows
  api-fetch     API fetch 50 results
  sheet-small   Google Sheets with 50 rows
        """
    )

    parser.add_argument(
        "scenarios",
        nargs="*",
        choices=list(SCENARIO_MEASUREMENTS.keys()),
        default=list(SCENARIO_MEASUREMENTS.keys()),
        help="Scenarios to compare (default: all)"
    )

    parser.add_argument(
        "--detail",
        metavar="SCENARIO",
        choices=list(SCENARIO_MEASUREMENTS.keys()),
        help="Show detailed example for a scenario"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Compliance threshold (default: 80%%)"
    )

    args = parser.parse_args()

    # Validate scenarios
    if args.detail and args.detail not in args.scenarios:
        args.scenarios.append(args.detail)

    # Output
    if args.json:
        print_json_output(args.scenarios)
    elif args.detail:
        print_detailed_example(args.detail)
    else:
        print_table(args.scenarios)

    # Check threshold compliance
    comparison = compare_scenarios(args.scenarios)
    avg_savings = comparison["summary"]["average_savings_percent"]
    meets_threshold = avg_savings >= args.threshold

    if not args.json and not args.detail:
        print("=" * 80)
        print(f"Compliance Check: {'PASS' if meets_threshold else 'FAIL'}")
        print(f"  Threshold: {args.threshold}%")
        print(f"  Actual: {avg_savings}%")
        print("=" * 80)

        sys.exit(0 if meets_threshold else 1)


if __name__ == "__main__":
    main()
