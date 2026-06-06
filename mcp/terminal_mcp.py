import subprocess
import os
from fastmcp import FastMCP

mcp = FastMCP(
    name="terminal-mcp",
    description="Full terminal access MCP server - run any command on the host"
)

@mcp.tool()
def run_command(cmd: str) -> str:
    """Run any shell command on the host terminal.
    Example: cmd = 'kubectl get pods -n three-tier-app'"""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=60
    )
    output = result.stdout.strip()
    error = result.stderr.strip()
    combined = ""
    if output:
        combined += output
    if error:
        combined += ("\n" if combined else "") + error
    return combined if combined else f"Done. Exit code: {result.returncode}"


@mcp.tool()
def apply_yaml(yaml_content: str) -> str:
    """Apply any Kubernetes YAML inline directly.
    Pass the full YAML content as a string."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        tmp_path = f.name
    result = subprocess.run(
        f"kubectl apply -f {tmp_path}",
        shell=True, capture_output=True, text=True, timeout=30
    )
    os.unlink(tmp_path)
    return result.stdout.strip() or result.stderr.strip()


@mcp.tool()
def read_file(path: str) -> str:
    """Read contents of any file on the host.
    Example: path = '/root/.kube/config'"""
    try:
        with open(os.path.expanduser(path), 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to any file on the host.
    Example: path = '/tmp/test.yaml'"""
    try:
        full_path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return f"Written to {full_path}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def install_package(package: str) -> str:
    """Install a Python package via pip or system package via apt.
    Example: package = 'pip:requests' or package = 'apt:curl'"""
    if package.startswith("apt:"):
        pkg = package[4:]
        cmd = f"apt-get install -y {pkg}"
    elif package.startswith("pip:"):
        pkg = package[4:]
        cmd = f"pip install {pkg}"
    else:
        cmd = f"pip install {package}"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=120
    )
    return result.stdout[-2000:] + result.stderr[-500:]


if __name__ == "__main__":
    print("Starting Terminal MCP Server on port 8001...")
    print("SSE endpoint: http://localhost:8001/sse")
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
