# k8s_deploy.py

## Overview

The `k8s_deploy.py` script manages Kubernetes deployments, services, and configurations. It provides automated deployment of applications with support for deployments, services, ConfigMaps, and Secrets.

## Features

- Kubernetes deployment management
- Service creation (ClusterIP, NodePort, LoadBalancer)
- ConfigMap and Secret management
- Namespace support
- YAML manifest generation
- Deployment monitoring

## Mermaid Diagram

```mermaid
flowchart TD
    A[Start: Kubernetes Deployment] --> B{Select Action}
    B -->|Deploy| C[Deployment Manager]
    B -->|Service| D[Service Manager]
    B -->|ConfigMap| E[ConfigMap Manager]
    B -->|Secret| F[Secret Manager]
    B -->|Apply| G[Manifest File]

    C --> H[Parse Deployment Spec]
    H --> I[Create Deployment]
    I --> J[Apply to Cluster]
    J --> K[Verify Status]
    K --> L[Return Result]

    D --> M[Parse Service Spec]
    M --> N[Create Service]
    N --> O[Apply to Cluster]
    O --> P[Verify Status]
    P --> Q[Return Result]

    E --> R[Parse ConfigMap Spec]
    R --> S[Create ConfigMap]
    S --> T[Apply to Cluster]
    T --> U[Verify Status]
    U --> V[Return Result]

    F --> W[Parse Secret Spec]
    W --> X[Create Secret]
    X --> Y[Apply to Cluster]
    Y --> Z[Verify Status]
    Z --> AA[Return Result]

    G --> AB[Read YAML File]
    AB --> AC[Parse Manifest]
    AC --> AD[Apply Manifest]
    AD --> AE[Verify Status]
    AE --> AF[Return Result]

    L --> AG[End]
    Q --> AG
    V --> AG
    AA --> AG
    AF --> AG
```

## Usage

### Deploy a Deployment

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    --deploy \
    --deployment myapp \
    --image myapp:latest \
    --replicas 3 \
    --port 8080
```

### Create a Service

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    service \
    --name web-service \
    --target myapp \
    --port 80 \
    --type LoadBalancer
```

### Create a ConfigMap

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    configmap \
    --name app-config \
    --data \
    DATABASE_URL=postgres://db:5432 \
    API_URL=https://api.example.com
```

### Create a Secret

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    secret \
    --name db-secret \
    --data \
    username=admin \
    password=secret123
```

### Apply from File

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    --deploy \
    --manifest k8s/deployment.yaml
```

## Commands

### Deploy

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    --deploy \
    --deployment myapp \
    --image nginx:latest \
    --replicas 3
```

### Service

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    service \
    --name api-service \
    --target myapp \
    --port 8080
```

### ConfigMap

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    configmap \
    --name app-config \
    --data key1=value1 key2=value2
```

### Secret

```bash
python scripts/k8s_deploy.py \
    --namespace production \
    secret \
    --name secret-credentials \
    --data username=user password=pass
```

## Architecture

```mermaid
classDiagram
    class KubernetesDeployer {
        -string namespace
        -string context
        +__init__(namespace: str)
        +create_namespace(name: str)
        +deploy_manifest(file: str, namespace: str)
        +deploy_deployment(name: str, image: str, replicas: int, namespace: str, port: int, env: Dict)
        +deploy_service(name: str, target: str, port: int, namespace: str, service_type: str)
        +deploy_configmap(name: str, data: Dict, namespace: str)
        +deploy_secret(name: str, data: Dict, namespace: str)
        +get_deployments(namespace: str) List
        +delete_deployment(name: str, namespace: str)
        +_write_and_deploy(manifest: Dict, name: str)
        +_get_current_context() str
    }

    class DeploymentSpec {
        +string apiVersion
        +string kind
        +Dict metadata
        +Dict spec
        +List containers
    }

    class ServiceSpec {
        +string apiVersion
        +string kind
        +Dict metadata
        +Dict spec
        +string type
        +Dict ports
        +Dict selector
    }

    class ConfigMapSpec {
        +string apiVersion
        +string kind
        +Dict metadata
        +Dict data
    }

    class SecretSpec {
        +string apiVersion
        +string kind
        +Dict metadata
        +string type
        +Dict data
    }

    KubernetesDeployer --> DeploymentSpec
    KubernetesDeployer --> ServiceSpec
    KubernetesDeployer --> ConfigMapSpec
    KubernetesDeployer --> SecretSpec
```

## Workflow

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant KubernetesDeployer
    participant API

    User->>Script: --namespace production
    Script->>KubernetesDeployer: KubernetesDeployer('production')
    KubernetesDeployer->>API: Create namespace
    API-->>KubernetesDeployer: Namespace ready
    KubernetesDeployer->>Script: Return

    User->>Script: --deploy --deployment myapp
    Script->>KubernetesDeployer: deploy_deployment()
    KubernetesDeployer->>KubernetesDeployer: _write_and_deploy()
    KubernetesDeployer->>API: Apply Deployment
    API-->>KubernetesDeployer: Deployment created
    KubernetesDeployer->>Script: Return status
```

## Configuration

### Environment Variables

- `KUBERNETES_NAMESPACE`: Default namespace (default: 'default')

### YAML Manifest Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 8080
          env:
            - name: ENV
              value: production
```

## Types of Services

### ClusterIP
Default service type for internal communication
```bash
python scripts/k8s_deploy.py service --name svc --target myapp --port 80 --type ClusterIP
```

### NodePort
Service accessible from outside cluster
```bash
python scripts/k8s_deploy.py service --name svc --target myapp --port 80 --type NodePort
```

### LoadBalancer
External load balancer for production
```bash
python scripts/k8s_deploy.py service --name svc --target myapp --port 80 --type LoadBalancer
```

## Return Codes

- `0`: Success
- `1`: Error

## Dependencies

- Python 3.7+
- kubectl
- Kubernetes cluster access
- PyYAML

## Examples

### Complete Deployment

```bash
# Create namespace
python scripts/k8s_deploy.py \
    --namespace production \
    --deploy \
    --deployment api-server \
    --image api-server:latest \
    --replicas 5 \
    --port 8080 \
    --env DATABASE_URL=postgres://db:5432 \
    --env ENVIRONMENT=production

# Create service
python scripts/k8s_deploy.py \
    --namespace production \
    service \
    --name api-service \
    --target api-server \
    --port 80

# Create configmap
python scripts/k8s_deploy.py \
    --namespace production \
    configmap \
    --name app-config \
    --data \
    DATABASE_URL=postgres://db:5432 \
    API_TIMEOUT=30
```

## Best Practices

1. **Use namespaces** to organize resources
2. **Always specify** image tags for reproducibility
3. **Use environment variables** for configuration
4. **Test manifests** before applying
5. **Monitor deployment** status after creation
