# LearnFlow Kubernetes MCP Server

MCP server providing Kubernetes operations for LearnFlow platform.

## Tools

1. **list_pods** - List pods in namespace with status (name, phase, ready, node)
2. **get_pod_logs** - Get recent pod logs (tail only, limited lines)
3. **list_services** - List services with endpoints and ports
4. **list_deployments** - List deployments with replica status
5. **get_pod_health** - Check if pod is ready and running
6. **get_learnflow_endpoints** - Get all LearnFlow service endpoints (ports 8100-8109, 8180)
7. **get_learnflow_deployments** - Get LearnFlow deployment status

## Token Efficiency

All operations return current status, not full historical data:
- **Pods**: Returns names, status, phases (not full pod specs)
- **Logs**: Returns last N lines only (not full history)
- **Deployments**: Returns replica counts, ready status (not full configs)

This achieves >80% token savings vs loading full k8s state.

## Installation

```bash
cd mcp-servers/k8s
npm install
npm run build
```

## Configuration

Requires kubeconfig file in ~/.kube/config or KUBECONFIG env variable.

## Usage

Add to Claude Code config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "learnflow-kubernetes": {
      "command": "node",
      "args": ["mcp-servers/k8s/dist/index.js"],
      "env": {
        "KUBECONFIG": "~/.kube/config"
      }
    }
  }
}
```

## Testing

Test with Claude Code:
```
/mcp-servers/k8s "List all LearnFlow pods"
/mcp-servers/k8s "Get LearnFlow service endpoints"
/mcp-servers/k8s "Check health of triage-service pod"
```
