# Kubernetes Error MCP Server

An MCP (Model Context Protocol) server that lets you apply, inspect, and debug Kubernetes error scenarios — all via HTTP/REST API with Swagger UI.

## Quick Start (KillerCoda / Linux)

```bash
# 1. Clone the repo
git clone https://github.com/nihallondhe/kubernetes-error-scenarios.git
cd kubernetes-error-scenarios/mcp

# 2. Build and run
docker-compose up --build
```

## Test in Browser

Open KillerCoda Traffic/Ports tab → Port 8000 → `/docs`

Or directly:
```
http://localhost:8000/docs
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_error_scenarios` | List all available error YAMLs |
| `apply_error` | Apply a specific error YAML to cluster |
| `get_pod_status` | Get all pod statuses |
| `get_events` | Get Warning events |
| `describe_pod` | Describe a specific pod |
| `delete_pod` | Force delete a pod |
| `get_node_status` | Get all node statuses |
| `check_pending_pods` | List Pending pods |
| `get_pod_logs` | Get pod logs |
| `cleanup_all_errors` | Delete all error pods at once |

## Requirements

- Docker + docker-compose
- `~/.kube/config` present (KillerCoda has this by default)
- `three-tier-app` namespace (create with `kubectl create namespace three-tier-app`)

## MCP Endpoint

```
http://localhost:8000/mcp
```
