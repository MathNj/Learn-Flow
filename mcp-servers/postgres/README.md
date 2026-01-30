# LearnFlow PostgreSQL MCP Server

MCP server providing database query tools for LearnFlow platform.

## Tools

1. **get_user_by_id** - Get user by ID (id, email, role, is_active)
2. **get_progress_summary** - Get student progress summary (total topics, mastered, avg mastery, streak)
3. **get_module_topics** - Get module topics with exercise/quiz counts and avg mastery
4. **get_struggling_students** - List struggling students by struggle threshold
5. **get_recent_submissions** - Get recent code submissions with scores

## Token Efficiency

All queries return aggregated summaries, not full datasets:
- **Progress**: Returns counts and averages (e.g., "5 topics, 2 mastered, 75% avg")
- **Struggling**: Returns student IDs and counts only
- **Submissions**: Returns metadata only (score, timestamp, exercise title)

This achieves >80% token savings vs loading full tables.

## Installation

```bash
cd mcp-servers/postgres
npm install
npm run build
```

## Configuration

Environment variables:
- `PGHOST` - PostgreSQL host (default: localhost)
- `PGPORT` - PostgreSQL port (default: 5432)
- `PGDATABASE` - Database name (default: learnflow)
- `PGUSER` - Database user (default: postgres)
- `PGPASSWORD` - Database password

## Usage

Add to Claude Code config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "learnflow-postgres": {
      "command": "node",
      "args": ["mcp-servers/postgres/dist/index.js"],
      "env": {
        "PGHOST": "localhost",
        "PGPORT": "5432",
        "PGDATABASE": "learnflow",
        "PGUSER": "postgres",
        "PGPASSWORD": "postgres"
      }
    }
  }
}
```

## Testing

Test with Claude Code:
```
/mcp-servers/postgres "Get student progress for student UUID"
```
