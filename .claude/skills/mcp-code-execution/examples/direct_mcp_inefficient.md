# Direct MCP Call: The Inefficient Anti-Pattern

This document shows the **wrong way** to work with MCP servers that return large datasets.

## The Problem: Token Bloat

When you call MCP servers directly, **ALL data flows into the agent context**:

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent Context                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tool Definitions: ~15,000 tokens                     │   │
│  │  ├── getSheet                                         │   │
│  │  ├── getRow                                           │   │
│  │  └── ... (20 more tools)                              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Data from MCP Server: ~35,000 tokens                 │   │
│  │  ├── Row 1, Row 2, Row 3, ... (10,000 rows)          │   │
│  │  └── All columns, all data                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  Remaining for your actual work: ~???                       │
└─────────────────────────────────────────────────────────────┘

Total: ~50,000+ tokens
```

## Example 1: Google Sheets

### Inefficient: Direct MCP Call

```python
# Agent code that loads ALL data into context

# Step 1: Load tool definitions (15,000 tokens)
tools = mcp_server.list_tools()

# Step 2: Call the tool (35,000 tokens)
sheet = mcp_server.call_tool("getSheet", {"id": "abc123"})

# Step 3: Agent processes in context (even more tokens!)
for row in sheet["data"]:
    if row["status"] == "pending":
        # Each loop iteration uses context
        process_row(row)
```

**Token Cost**:
- Tool definitions: 15,000 tokens
- Sheet data (10,000 rows): 35,000 tokens
- Processing overhead: Variable
- **Total: ~50,000+ tokens**

### What's Wrong?

1. **All 10,000 rows** are loaded into context
2. **Filtering happens in context** (after data is loaded)
3. **Most data is discarded** (only 5 rows needed)
4. **Token cost is the same** whether you need 1 row or all 10,000

## Example 2: Kubernetes Pods

### Inefficient: Direct kubectl via MCP

```python
# Agent loads ALL pod data into context

# Get all pods across all namespaces
pods = mcp_kubectl.run("kubectl get pods -A")

# Now filter in context (already too late!)
running_pods = [p for p in pods if p["status"] == "Running"]

# Get details (more tokens!)
for pod in running_pods:
    details = mcp_kubectl.run(f"kubectl describe pod {pod['name']}")
```

**Token Cost**:
- 100 pods × 150 tokens each: 15,000 tokens
- Descriptions add more: 5,000+ tokens
- **Total: ~20,000+ tokens**

## Example 3: File Repository Scan

### Inefficient: Direct MCP File Access

```python
# Agent loads ALL file contents into context

# List all files (1,000 files)
files = mcp_fs.listFiles({"path": "./src", "recursive": True})

# Read each file (in context!)
for file in files:
    content = mcp_fs.readFile(file["path"])
    if "TODO" in content:
        # Each file content loaded into context
        todos.append(file)
```

**Token Cost**:
- File list: 5,000 tokens
- File contents: 20,000 tokens (average 20 tokens × 1,000 files)
- **Total: ~25,000+ tokens**

## Visual Comparison

```
Direct MCP Call:
┌────────┐     ┌────────┐     ┌──────────┐
│ Agent  │────>│  MCP   │────>│ 50K+     │
│        │<────│ Server │<────│ tokens   │
└────────┘     └────────┘     └──────────┘
               (ALL data
                flows to
                context)

Code Execution Pattern:
┌────────┐     ┌────────┐     ┌──────────┐
│ Agent  │────>│ Script │────>│ MCP      │
│        │<────│        │     │ Server   │
└────────┘  ~50 └────────┘     └──────────┘
   tokens          (script executes
                    outside context)
```

## The Core Problem

**Direct MCP calls violate the principle of "load only what you need"**:

| Aspect | Direct MCP | Problem |
|--------|------------|---------|
| Data loading | ALL data | Most is discarded |
| Filtering | In context | After tokens spent |
| Cost | Fixed high | Same for 1 or 10K rows |
| Scalability | Poor degrades | Larger datasets = worse |

## Common Anti-Patterns

### Anti-Pattern 1: Loop Over MCP Results

```python
# WRONG: Loop loads data into context
for row in mcp.getSheet("abc123"):
    if row["status"] == "pending":
        # Each iteration uses context
        process(row)
```

### Anti-Pattern 2: Chained MCP Calls

```python
# WRONG: Each call adds to context
sheet = mcp.getSheet("abc123")      # 35K tokens
users = mcp.getUsers()              # 10K tokens
tasks = mcp.getTasks()              # 15K tokens
# Total: 60K+ tokens in context
```

### Anti-Pattern 3: MCP Data Transformation in Context

```python
# WRONG: Transform after loading
data = mcp.getSheet("abc123")       # 35K tokens
transformed = transform(data)       # More tokens
aggregated = aggregate(transformed) # Even more
```

## What You Should Do Instead

See `code_execution_efficient.md` for the correct pattern.

**Key insight**: Process data **outside** agent context, return **only results**.

```python
# RIGHT: Script processes, returns minimal results
result = subprocess.run([
    "python", "scripts/filter_sheet.py",
    "--sheet-id", "abc123",
    "--status", "pending",
    "--limit", "5"
], capture_output=True)

# Only 5 rows in context (~50 tokens)
filtered = json.loads(result.stdout)
```

**Token savings: 99.9%** (50,000 → 50 tokens)
