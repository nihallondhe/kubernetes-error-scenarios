FROM python:3.12-slim

# Install kubectl
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -LO "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && mv kubectl /usr/local/bin/kubectl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone error scenarios from GitHub at build time
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/nihallondhe/kubernetes-error-scenarios.git /app/scenarios && \
    apt-get remove -y git && apt-get autoremove -y && apt-get clean

COPY mcp_server.py .

EXPOSE 8000

CMD ["python", "mcp_server.py"]
