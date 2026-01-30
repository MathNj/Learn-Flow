# LearnFlow Kafka MCP Server

MCP server providing Kafka operations for LearnFlow platform.

## Tools

1. **list_topics** - List all Kafka topics with partition count
2. **get_topic_message_counts** - Get message counts for topics (aggregated)
3. **get_consumer_group_lag** - Get consumer lag information (summarized by group)
4. **get_topic_partition_info** - Get partition metadata (leader, replicas, ISR)
5. **list_consumer_groups** - List all consumer groups with member count

## Token Efficiency

All operations return metadata and aggregated counts, not message payloads:
- **Topic Counts**: Returns message counts only (not full messages)
- **Consumer Lag**: Returns aggregated totals by group
- **Partition Info**: Returns metadata only (leader, replicas)

This achieves >80% token savings vs loading topic data.

## Installation

```bash
cd mcp-servers/kafka
npm install
npm run build
```

## Configuration

Environment variables:
- `KAFKA_BROKERS` - Kafka brokers (default: localhost:9092)

## Usage

Add to Claude Code config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "learnflow-kafka": {
      "command": "node",
      "args": ["mcp-servers/kafka/dist/index.js"],
      "env": {
        "KAFKA_BROKERS": "localhost:9092"
      }
    }
  }
}
```

## Testing

Test with Claude Code:
```
/mcp-servers/kafka "List all Kafka topics"
/mcp-servers/kafka "Get consumer lag for all groups"
```
