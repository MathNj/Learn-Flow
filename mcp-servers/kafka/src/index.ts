#!/usr/bin/env node
/**
 * LearnFlow Kafka MCP Server
 *
 * Provides MCP tools for Kafka operations:
 * - List topics and consumer groups
 * - Get topic message counts
 * - Consumer lag monitoring
 * - Message inspection (limited for token efficiency)
 *
 * Token Efficiency: Returns aggregated counts and summaries, not full message payloads
 * Target: >80% token savings vs direct topic data loading
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Kafka, logLevel } from "kafkajs";

// Kafka client configuration
const kafka = new Kafka({
  clientId: "learnflow-mcp-server",
  brokers: [process.env.KAFKA_BROKERS || "localhost:9092"],
  logLevel: logLevel.ERROR,
});

const admin = kafka.admin();

/**
 * Get topic message counts (aggregated, not individual messages)
 * Token Efficient: Returns counts only, not message payloads
 */
async function getTopicMessageCounts(topics: string[]) {
  const consumer = kafka.consumer({ groupId: "temp-inspector" });

  const counts: Record<string, number> = {};

  for (const topic of topics) {
    try {
      await consumer.connect();
      const { offsets } = await consumer.fetchOffsets({
        topics: [topic],
      });

      if (offsets && offsets[topic] && offsets[topic].length > 0) {
        // Calculate lag from earliest to latest offset
        const earliest = offsets[topic][0].offset;
        const latest = offsets[topic][offsets[topic].length - 1].offset;
        counts[topic] = latest - earliest;
      } else {
        counts[topic] = 0;
      }
    } catch (error) {
      counts[topic] = 0;
    } finally {
      await consumer.disconnect();
    }
  }

  return counts;
}

/**
 * List all topics (metadata only, no messages)
 */
async function listTopics() {
  const topics = await admin.listTopics();
  return topics.map((topic) => ({
    name: topic,
    partitions: topic.partitions,
  }));
}

/**
 * Get consumer group lag (aggregated summary)
 */
async function getConsumerGroupLag() {
  const groups = await admin.listConsumerGroups();
  const groupIds = groups.map((g) => g.groupId);

  const lagInfo: Array<{
    groupId: string;
    lag: number;
    topic: string;
    partition: number;
  }> = [];

  for (const groupId of groupIds) {
    try {
      const offsets = await admin.fetchOffsets({
        groupId,
      });

      for (const topicOffset of offsets) {
        for (const partitionOffset of topicOffset.partitions) {
          lagInfo.push({
            groupId,
            lag: partitionOffset.lag,
            topic: topicOffset.topic,
            partition: partitionOffset.partition,
          });
        }
      }
    } catch (error) {
      // Skip groups we can't fetch
      continue;
    }
  }

  // Aggregate by group for token efficiency
  const aggregated: Record<string, { totalLag: number; topicCount: number }> = {};
  for (const info of lagInfo) {
    if (!aggregated[info.groupId]) {
      aggregated[info.groupId] = { totalLag: 0, topicCount: 0 };
    }
    aggregated[info.groupId].totalLag += info.lag;
    aggregated[info.groupId].topicCount++;
  }

  return aggregated;
}

/**
 * Get topic partition info (metadata only)
 */
async function getTopicPartitionInfo(topic: string) {
  const partitionMetadata = await admin.describeClusters();
  const clusterId = partitionMetadata.clusters[0].clusterId;
  const topicMetadata = await admin.describeTopics({ topics: [topic] });

  if (topicMetadata.topics.length === 0) {
    throw new Error(`Topic ${topic} not found`);
  }

  return topicMetadata.topics[0].partitions.map((p) => ({
    partition: p.partition,
    leader: p.leader,
    replicas: p.replicas,
    isr: p.isr,
  }));
}

/**
 * Get consumer groups list (names only)
 */
async function listConsumerGroups() {
  const groups = await admin.listConsumerGroups();
  return groups.map((g) => ({
    groupId: g.groupId,
    members: g.members.length,
    state: g.state,
  }));
}

// Create MCP server
const server = new Server(
  {
    name: "learnflow-kafka",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

server.setRequestHandler(async (request) => {
  const { method, params } = request;

  if (method === "tools/list") {
    return {
      tools: [
        {
          name: "list_topics",
          description: "List all Kafka topics with partition count",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "get_topic_message_counts",
          description: "Get message counts for specified topics (aggregated, no message payloads)",
          inputSchema: {
            type: "object",
            properties: {
              topics: {
                type: "array",
                items: { type: "string" },
                description: "Topic names to count",
              },
            },
            required: ["topics"],
          },
        },
        {
          name: "get_consumer_group_lag",
          description: "Get consumer group lag information (aggregated summary by group)",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "get_topic_partition_info",
          description: "Get partition metadata for a topic (leader, replicas, ISR)",
          inputSchema: {
            type: "object",
            properties: {
              topic: {
                type: "string",
                description: "Topic name",
              },
            },
            required: ["topic"],
          },
        },
        {
          name: "list_consumer_groups",
          description: "List all consumer groups with member count and state",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
      ],
    };
  }

  if (method === "tools/call") {
    const { name, arguments } = params;

    try {
      switch (name) {
        case "list_topics":
          const topics = await listTopics();
          return {
            content: [{
              type: "text",
              text: JSON.stringify(topics, null, 2),
            }],
          };

        case "get_topic_message_counts":
          const counts = await getTopicMessageCounts(
            arguments.topics as string[]
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(counts, null, 2),
            }],
          };

        case "get_consumer_group_lag":
          const lag = await getConsumerGroupLag();
          return {
            content: [{
              type: "text",
              text: JSON.stringify(lag, null, 2),
            }],
          };

        case "get_topic_partition_info":
          const partitionInfo = await getTopicPartitionInfo(
            arguments.topic as string
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(partitionInfo, null, 2),
            }],
          };

        case "list_consumer_groups":
          const groups = await listConsumerGroups();
          return {
            content: [{
              type: "text",
              text: JSON.stringify(groups, null, 2),
            }],
          };

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            error: error instanceof Error ? error.message : String(error),
          }),
        }],
        isError: true,
      };
    }
  }

  return {};
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("LearnFlow Kafka MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
