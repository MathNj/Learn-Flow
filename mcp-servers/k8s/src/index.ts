#!/usr/bin/env node
/**
 * LearnFlow Kubernetes MCP Server
 *
 * Provides MCP tools for Kubernetes operations:
 * - List pods, services, deployments
 * - Get pod logs (tail only, not full history for token efficiency)
 * - Get service endpoints
 * - Check pod health status
 *
 * Token Efficiency: Returns current status and recent logs, not full histories
 * Target: >80% token savings vs loading full k8s state
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as k8s from "@kubernetes/client-node";
import * as yaml from "yaml";

// Load kubeconfig
const kc = new k8s.KubeConfig();
kc.loadFromDefault();

// Create Kubernetes clients
const k8sApi = kc.makeApiClient(k8s.CoreV1Api);
const appsV1Api = kc.makeApiClient(k8s.AppsV1Api);

/**
 * List pods in namespace (summary only)
 * Token Efficient: Returns names, status, phases - not full pod specs
 */
async function listPods(namespace: string = "default") {
  const podList = await k8sApi.listNamespacedPod(namespace);
  return podList.body.items.map((pod) => ({
    name: pod.metadata.name,
    namespace: pod.metadata.namespace,
    phase: pod.status.phase,
    nodeName: pod.spec.nodeName,
    ready: pod.status.containerStatuses?.every(
      (cs) => cs.ready === true
    ),
  }));
}

/**
 * Get pod logs (tail only, limited lines)
 * Token Efficient: Returns last N lines, not full history
 */
async function getPodLogs(
  namespace: string,
  podName: string,
  tailLines: number = 50
): Promise<string> {
  const logs = await k8sApi.readNamespacedPodLog(
    namespace,
    podName,
    undefined, // container name (default to first container)
    undefined, // tail
    undefined, // limitBytes
    tailLines
  );

  return logs.body;
}

/**
 * Get services in namespace (endpoints only)
 */
async function getServices(namespace: string = "default") {
  const serviceList = await k8sApi.listNamespacedService(namespace);
  return serviceList.body.items.map((service) => ({
    name: service.metadata.name,
    namespace: service.metadata.namespace,
    type: service.spec.type,
    clusterIP: service.spec.clusterIP,
    ports: service.spec.ports.map((p) => ({
      port: p.port,
      protocol: p.protocol,
      targetPort: p.targetPort,
    })),
  }));
}

/**
 * Get deployments in namespace (summary)
 */
async function getDeployments(namespace: string = "default") {
  const deployList = await appsV1Api.listNamespacedDeployment(namespace);
  return deployList.body.items.map((deploy) => ({
    name: deploy.metadata.name,
    namespace: deploy.metadata.namespace,
    replicas: deploy.spec.replicas,
    availableReplicas: deploy.status.availableReplicas || 0,
    ready: (deploy.status.readyReplicas || 0) === (deploy.spec.replicas || 0),
    updatedAt: deploy.status.conditions?.[0]?.lastUpdateTime,
  }));
}

/**
 * Get pod health status (simple ready check)
 */
async function getPodHealth(namespace: string, podName: string) {
  try {
    const pod = await k8sApi.readNamespacedPod(namespace, podName);

    const isReady = pod.status.phase === "Running" &&
      pod.status.containerStatuses?.every(
        (cs) => cs.ready === true && cs.state === "running"
      );

    return {
      name: pod.metadata.name,
      namespace: pod.metadata.namespace,
      phase: pod.status.phase,
      ready: isReady,
      restartCount: pod.status.containerStatuses?.[0].restartCount || 0,
    };
  } catch (error) {
    return {
      name: podName,
      namespace,
      phase: "Unknown",
      ready: false,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

/**
 * Get LearnFlow service endpoints (aggregated)
 */
async function getLearnFlowEndpoints() {
  const services = await getServices("default");

  // Filter LearnFlow services (ports 8100-8109, 8180)
  const learnflowServices = services.filter((s) =>
    s.ports.some((p) =>
      (p.port >= 8100 && p.port <= 8109) || p.port === 8180
    )
  );

  return learnflowServices.map((s) => ({
    name: s.name,
    type: s.type,
    ports: s.ports.map((p) => ({
      port: p.port,
      protocol: p.protocol,
      url: s.clusterIP ? `${s.clusterIP}:${p.port}` : null,
    })),
  }));
}

/**
 * Get LearnFlow deployment status
 */
async function getLearnFlowDeployments() {
  const deployments = await getDeployments("default");

  // Filter LearnFlow deployments
  const learnflowDeployments = deployments.filter((d) =>
    d.name.includes("service") || d.name.includes("agent")
  );

  return learnflowDeployments.map((d) => ({
    name: d.name,
    replicas: d.replicas,
    available: d.availableReplicas,
    ready: d.ready,
  }));
}

// Create MCP server
const server = new Server(
  {
    name: "learnflow-kubernetes",
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
          name: "list_pods",
          description: "List all pods in namespace with status (name, phase, ready, node)",
          inputSchema: {
            type: "object",
            properties: {
              namespace: {
                type: "string",
                description: "Kubernetes namespace (default: default)",
              },
            },
          },
        },
        {
          name: "get_pod_logs",
          description: "Get recent pod logs (tail only, limited lines for token efficiency)",
          inputSchema: {
            type: "object",
            properties: {
              namespace: {
                type: "string",
                description: "Kubernetes namespace (default: default)",
              },
              podName: {
                type: "string",
                description: "Pod name",
              },
              tailLines: {
                type: "number",
                description: "Number of log lines to return (default: 50)",
              },
            },
            required: ["podName"],
          },
        },
        {
          name: "list_services",
          description: "List all services with endpoints and ports",
          inputSchema: {
            type: "object",
            properties: {
              namespace: {
                type: "string",
                description: "Kubernetes namespace (default: default)",
              },
            },
          },
        },
        {
          name: "list_deployments",
          description: "List deployments with replica status",
          inputSchema: {
            type: "object",
            properties: {
              namespace: {
                type: "string",
                description: "Kubernetes namespace (default: default)",
              },
            },
          },
        },
        {
          name: "get_pod_health",
          description: "Check if pod is ready and running",
          inputSchema: {
            type: "object",
            properties: {
              namespace: {
                type: "string",
                description: "Kubernetes namespace (default: default)",
              },
              podName: {
                type: "string",
                description: "Pod name",
              },
            },
            required: ["podName"],
          },
        },
        {
          name: "get_learnflow_endpoints",
          description: "Get all LearnFlow service endpoints (ports 8100-8109, 8180)",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "get_learnflow_deployments",
          description: "Get LearnFlow deployment status (replicas, ready state)",
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
        case "list_pods":
          const pods = await listPods(
            (arguments.namespace as string) || "default"
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(pods, null, 2),
            }],
          };

        case "get_pod_logs":
          const logs = await getPodLogs(
            (arguments.namespace as string) || "default",
            arguments.podName as string,
            arguments.tailLines as number || 50
          );
          return {
            content: [{
              type: "text",
              text: logs,
            }],
          };

        case "list_services":
          const services = await getServices(
            (arguments.namespace as string) || "default"
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(services, null, 2),
            }],
          };

        case "list_deployments":
          const deployments = await getDeployments(
            (arguments.namespace as string) || "default"
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(deployments, null, 2),
            }],
          };

        case "get_pod_health":
          const health = await getPodHealth(
            (arguments.namespace as string) || "default",
            arguments.podName as string
          );
          return {
            content: [{
              type: "text",
              text: JSON.stringify(health, null, 2),
            }],
          };

        case "get_learnflow_endpoints":
          const endpoints = await getLearnflowEndpoints();
          return {
            content: [{
              type: "text",
              text: JSON.stringify(endpoints, null, 2),
            }],
          };

        case "get_learnflow_deployments":
          const deployments = await getLearnFlowDeployments();
          return {
            content: [{
              type: "text",
              text: JSON.stringify(deployments, null, 2),
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
  console.error("LearnFlow Kubernetes MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
