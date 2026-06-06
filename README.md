# Kubernetes Error Scenarios

A collection of Kubernetes manifests that intentionally trigger common error states for learning and debugging practice.

## Folder Structure

```
kubernetes-error-scenarios/
├── pod-errors/         # Pod-level failures
├── db-errors/          # Database (StatefulSet/PVC) failures
└── node-errors/        # Node scheduling failures
```

## Pod Errors

| File | Error Type | Description |
|------|-----------|-------------|
| pod-issue-crashloop.yaml | CrashLoopBackOff | Container exits immediately |
| pod-issue-imagepull.yaml | ImagePullBackOff | Invalid image tag |
| pod-issue-pending.yaml | Pending | Impossible resource requests |
| pod-issue-configerror.yaml | CreateContainerConfigError | Missing ConfigMap reference |
| pod-issue-oomkilled.yaml | OOMKilled | Memory limit exceeded |
| pod-issue-probefail.yaml | Liveness probe fail | Wrong probe path causes restart loop |

## DB Errors

| File | Error Type | Description |
|------|-----------|-------------|
| db-issue-crashloop.yaml | CrashLoopBackOff | Empty Postgres password |
| db-issue-imagepull.yaml | ImagePullBackOff | Invalid image tag |
| db-issue-pending-pvc.yaml | Pending PVC | Non-existent StorageClass |

## Node Errors

| File | Error Type | Description |
|------|-----------|-------------|
| node-issue-nodeselector-mismatch.yaml | FailedScheduling | nodeSelector matches no node |
| node-issue-nodeaffinity-mismatch.yaml | FailedScheduling | nodeAffinity requires GPU label |
| node-issue-missing-toleration.yaml | FailedScheduling | No toleration for tainted node |
| node-issue-impossible-combo.yaml | FailedScheduling | Windows OS + arm64 arch combo |
| node-issue-fixed-nodename.yaml | FailedScheduling | nodeName set to nonexistent node |

## Usage

```bash
# Apply a specific error
kubectl apply -f pod-errors/pod-issue-crashloop.yaml

# Watch in real time
kubectl get pods -n three-tier-app -w

# Watch events
kubectl get events -n three-tier-app -w --field-selector type=Warning

# Describe failing pod
kubectl describe pod <pod-name> -n three-tier-app
```

## Namespace

All manifests target the `three-tier-app` namespace. Create it first if needed:

```bash
kubectl create namespace three-tier-app
```
