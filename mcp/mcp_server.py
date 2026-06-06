import subprocess
import os
from fastmcp import FastMCP

mcp = FastMCP(
    name="kubernetes-error-mcp",
    description="MCP server to apply and debug Kubernetes error scenarios"
)

NAMESPACE = "three-tier-app"
REPO_DIR = "/app/scenarios"

def run(cmd: str) -> str:
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=30
    )
    output = result.stdout.strip()
    error  = result.stderr.strip()
    if result.returncode != 0:
        return f"ERROR:\n{error}" if error else f"Exit code {result.returncode}"
    return output if output else (error if error else "Done.")


@mcp.tool()
def list_error_scenarios() -> str:
    """List all available Kubernetes error scenario YAML files."""
    output = []
    for folder in ["pod-errors", "db-errors", "node-errors"]:
        path = os.path.join(REPO_DIR, folder)
        if os.path.isdir(path):
            files = sorted(os.listdir(path))
            output.append(f"\n\U0001f4c1 {folder}:")
            for f in files:
                if f.endswith(".yaml"):
                    output.append(f"  - {folder}/{f}")
    return "\n".join(output) if output else "No scenarios found."


@mcp.tool()
def apply_error(scenario: str) -> str:
    """Apply a Kubernetes error scenario YAML.
    Example scenario: pod-errors/pod-issue-crashloop.yaml"""
    yaml_path = os.path.join(REPO_DIR, scenario)
    if not os.path.exists(yaml_path):
        return f"File not found: {scenario}. Use list_error_scenarios to see available files."
    return run(f"kubectl apply -f {yaml_path}")


@mcp.tool()
def get_pod_status() -> str:
    """Get real-time status of all pods in the three-tier-app namespace."""
    return run(f"kubectl get pods -n {NAMESPACE} -o wide")


@mcp.tool()
def get_events() -> str:
    """Get all Warning events from the three-tier-app namespace."""
    return run(
        f"kubectl get events -n {NAMESPACE} "
        f"--field-selector type=Warning "
        f"--sort-by=.lastTimestamp"
    )


@mcp.tool()
def describe_pod(pod_name: str) -> str:
    """Describe a specific pod to see detailed status and events.
    Example pod_name: pod-bad-crashloop"""
    return run(f"kubectl describe pod {pod_name} -n {NAMESPACE}")


@mcp.tool()
def delete_pod(pod_name: str) -> str:
    """Delete/cleanup a specific pod from the three-tier-app namespace.
    Example pod_name: pod-bad-crashloop"""
    return run(f"kubectl delete pod {pod_name} -n {NAMESPACE} --grace-period=0 --force")


@mcp.tool()
def get_node_status() -> str:
    """Get status of all nodes in the cluster."""
    return run("kubectl get nodes -o wide")


@mcp.tool()
def check_pending_pods() -> str:
    """List all pods currently in Pending state in three-tier-app namespace."""
    return run(
        f"kubectl get pods -n {NAMESPACE} "
        f"--field-selector=status.phase=Pending -o wide"
    )


@mcp.tool()
def get_pod_logs(pod_name: str) -> str:
    """Get logs from a specific pod.
    Example pod_name: pod-bad-crashloop"""
    return run(f"kubectl logs {pod_name} -n {NAMESPACE} --tail=50 --previous 2>/dev/null || "
               f"kubectl logs {pod_name} -n {NAMESPACE} --tail=50")


@mcp.tool()
def cleanup_all_errors() -> str:
    """Delete all error scenario pods and statefulsets from the namespace."""
    cmds = [
        f"kubectl delete pod node-bad-selector node-bad-affinity node-bad-taint "
        f"node-bad-impossible-combo node-bad-nodename "
        f"pod-bad-crashloop pod-bad-imagepull pod-bad-pending "
        f"pod-bad-configerror pod-bad-oomkilled pod-bad-probefail "
        f"-n {NAMESPACE} --grace-period=0 --force --ignore-not-found",
        f"kubectl delete statefulset postgres-bad-crash postgres-bad-image postgres-bad-pvc "
        f"-n {NAMESPACE} --ignore-not-found",
    ]
    results = []
    for cmd in cmds:
        results.append(run(cmd))
    return "\n".join(results)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path="/mcp")
