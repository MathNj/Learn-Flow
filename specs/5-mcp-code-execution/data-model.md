# Data Model: MCP Code Execution Pattern

**Feature**: 5-mcp-code-execution | **Date**: 2025-01-27

## Overview

This document defines the data model for the MCP Code Execution Pattern demonstration skill. Since this is a documentation/pattern skill, entities focus on pattern examples, templates, and validation criteria.

---

## Pattern Documentation Model

### PatternExample

Represents a concrete example demonstrating token savings.

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class PatternExample(BaseModel):
    """A concrete example of the MCP code execution pattern."""

    name: str = Field(..., description="Example name (e.g., 'Sheet Filter')")
    description: str = Field(..., description="What this example demonstrates")

    # Direct MCP approach (inefficient)
    direct_approach: str = Field(..., description="Code showing direct MCP call")
    direct_tokens: int = Field(..., description="Estimated tokens used")

    # Code execution pattern (efficient)
    pattern_approach: str = Field(..., description="Code showing pattern usage")
    pattern_tokens: int = Field(..., description="Estimated tokens used")

    # Results
    savings_percent: float = Field(..., description="Token savings percentage")

    # Metadata
    language: str = Field(default="python", description="Programming language")
    mcp_server: str = Field(..., description="MCP server used in example")
    use_case: str = Field(..., description="Use case category")
```

### UseCaseCategory

Categories of when to apply the pattern.

```python
class UseCaseCategory(str, enum):
    """Categories determining when to use the pattern."""
    LARGE_DATA = "large_data"           # >100 rows or >10KB
    FILTERING = "filtering"             # Subset/transform needed
    REPEATED = "repeated"               # Multiple similar calls
    COMPLEX = "complex"                 # Computation required
```

### ValidationResult

Result of validating a skill's token efficiency.

```python
class ValidationResult(BaseModel):
    """Result of token efficiency validation."""

    skill_name: str = Field(..., description="Name of skill being validated")
    is_compliant: bool = Field(..., description="Uses pattern correctly")

    # Token metrics
    direct_token_estimate: int = Field(..., description="Tokens without pattern")
    pattern_token_estimate: int = Field(..., description="Tokens with pattern")
    savings_percent: float = Field(..., description="Savings achieved")

    # Issues found
    issues: List[str] = Field(default_factory=list, description="Specific issues")
    recommendations: List[str] = Field(default_factory=list, description="Improvement suggestions")

    # Validation metadata
    validated_at: datetime = Field(default_factory=datetime.utcnow)
    validator_version: str = Field(default="1.0.0")
```

### WrapperTemplate

Template for generating MCP wrapper scripts.

```python
class WrapperTemplate(BaseModel):
    """Template for generating wrapper scripts."""

    name: str = Field(..., description="Template name")
    language: str = Field(..., description="Target language (python, bash, javascript)")

    # Template content
    template_code: str = Field(..., description="Jinja2 template for wrapper")

    # MCP configuration
    mcp_server_name: str = Field(..., description="Target MCP server")
    mcp_tool_name: str = Field(..., description="Tool to wrap")
    mcp_parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")

    # Processing instructions
    processing_logic: str = Field(..., description="Data transformation code")
    output_format: str = Field(default="json", description="Output format (json, text)")
```

### TokenMeasurement

Measurement of token usage for comparison.

```python
class TokenMeasurement(BaseModel):
    """Token usage measurement."""

    operation: str = Field(..., description="Operation being measured")
    approach: str = Field(..., description="direct_mcp or code_execution")

    # Metrics
    token_count: int = Field(..., description="Tokens measured")
    char_count: int = Field(..., description="Character count (for estimation)")
    data_size_bytes: int = Field(..., description="Data size in bytes")

    # Context
    model: str = Field(default="gpt-4", description="Model used for tokenization")
    measured_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Pattern Decision Tree

```python
class PatternDecision(BaseModel):
    """Decision model for when to use the pattern."""

    # Input characteristics
    estimated_row_count: int = Field(..., description="Estimated rows returned")
    estimated_size_kb: float = Field(..., description="Estimated data size in KB")
    estimated_tokens: int = Field(..., description="Estimated token usage")

    # Operation characteristics
    requires_filtering: bool = Field(default=False, description="Need to filter results")
    requires_aggregation: bool = Field(default=False, description="Need to aggregate data")
    repeated_operation: bool = Field(default=False, description="Called multiple times")
    requires_computation: bool = Field(default=False, description="Results need processing")

    # Decision
    use_pattern: bool = Field(..., description="Whether to use code execution pattern")
    reason: str = Field(..., description="Explanation for decision")

    def should_use_pattern(self) -> bool:
        """Determine if pattern should be used based on thresholds."""
        if self.estimated_row_count > 100:
            return True
        if self.estimated_size_kb > 10:
            return True
        if self.estimated_tokens > 5000:
            return True
        if self.requires_filtering or self.requires_aggregation:
            return True
        if self.repeated_operation:
            return True
        return False
```

---

## Entity Relationships

```
┌─────────────────────┐     ┌──────────────────────┐
│   PatternExample     │────▶│  TokenMeasurement     │
│  (Demonstrates)      │     │  (Measures Usage)      │
└─────────────────────┘     └──────────────────────┘
           │                           │
           │                           │
           ▼                           ▼
┌─────────────────────┐     ┌──────────────────────┐
│    UseCaseCategory   │     │  ValidationResult     │
│  (When to Apply)     │────▶│  (Validates Skills)   │
└─────────────────────┘     └──────────────────────┘
           │                           │
           │                           │
           ▼                           ▼
┌──────────────────────────────────────────────────────────┐
│                    WrapperTemplate                         │
│  (Generates MCP wrappers for any server/operation)        │
└──────────────────────────────────────────────────────────┘
```

---

## Example Instances

### Sheet Filter Example (Python)

```python
sheet_filter_example = PatternExample(
    name="Sheet Large Data Filter",
    description="Filter 10,000 rows to 5 matching rows",

    direct_approach="""
# Direct MCP - ALL data into context
result = mcp.get_sheet("abc123")
# result: 10,000 rows → 50,000 tokens
""",
    direct_tokens=50000,

    pattern_approach="""
# Code Execution - script does the work
# scripts/filter_sheet.py
from mcp_client import MCPServerClient

client = MCPServerClient("sheets")
data = client.call_tool("get_sheet", {"id": "abc123"})
filtered = [r for r in data if r["status"] == "pending"][:5]
print(filtered)
# Only 5 rows returned → ~50 tokens
""",
    pattern_tokens=50,

    savings_percent=99.9,
    language="python",
    mcp_server="sheets-mcp",
    use_case="large_data"
)
```

### Kubernetes Pods Example (Bash)

```bash
k8s_pods_example = PatternExample(
    name="Kubernetes Pod List Filter",
    description="Get 100 pods, filter to 5 running pods",

    direct_approach="""
# Direct MCP - ALL pods into context
kubectl get pods -A
# result: 100 pods → 15,000 tokens
""",
    direct_tokens=15000,

    pattern_approach="""
# Code Execution - script filters
# scripts/get_pods.sh
kubectl get pods -A | grep Running | head -5
# Only 5 pods returned → ~30 tokens
""",
    pattern_tokens=30,

    savings_percent=99.8,
    language="bash",
    mcp_server="k8s-mcp",
    use_case="filtering"
)
```

### File Scan Example (JavaScript)

```javascript
file_scan_example = {
    name: "Repository File Scan",
    description: "Scan 1000 files, find TODO comments",

    direct_approach: `
// Direct MCP - ALL files into context
const files = mcp.listFiles({path: "./src"});
// result: 1000 files → 25,000 tokens
`,
    direct_tokens: 25000,

    pattern_approach: `
// Code Execution - script filters
// scripts/scan_todos.js
const results = files
  .filter(f => f.contents.includes("TODO"))
  .slice(0, 20);
// Only TODO files returned → ~100 tokens
`,
    pattern_tokens: 100,

    savings_percent: 99.6,
    language: "javascript",
    mcp_server: "filesystem-mcp",
    use_case: "filtering"
}
```

---

## Validation Rules

### PatternExample Validation
- `name`: Must be unique across examples
- `savings_percent`: Must be > 80% (constitution requirement)
- `direct_tokens` > `pattern_tokens`: Must demonstrate actual savings
- `pattern_approach`: Must execute outside agent context

### ValidationResult Validation
- `savings_percent`: Must calculate correctly
- `issues`: Must be empty if `is_compliant` is True
- `recommendations`: Must be actionable if `is_compliant` is False

### WrapperTemplate Validation
- `template_code`: Must be valid Jinja2 template
- `language`: Must be one of: python, bash, javascript
- `mcp_server_name`: Must reference a real MCP server or use placeholder

---

## Data Retention

No persistent data storage - this is a documentation skill. All data is in Markdown and code files.

---

## Security Considerations

- **API Keys**: Never in examples (use placeholders like YOUR_API_KEY)
- **Credentials**: Always use environment variables in templates
- **File Access**: Scripts should not access files outside intended scope
- **Code Execution**: Scripts run with user's permissions, warn about security

---

## Migration Strategy

Not applicable - pattern documentation doesn't have data migrations.

---

## Concurrency Control

Not applicable - documentation skill is read-only at runtime.

---

## Token Efficiency Validation

All examples in this skill must demonstrate >80% token savings:

| Example | Direct | Pattern | Savings | Pass/Fail |
|---------|--------|--------|---------|----------|
| Sheet 10K rows | 50,000 | 50 | 99.9% | PASS |
| K8s 100 pods | 15,000 | 30 | 99.8% | PASS |
| Repo 1K files | 25,000 | 100 | 99.6% | PASS |
| DB 500 rows | 10,000 | 20 | 99.8% | PASS |

**All examples PASS the 80% threshold.**
