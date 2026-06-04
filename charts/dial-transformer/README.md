# Dial Transformer Helm Chart

This Helm chart deploys the DIAL Transformer service, an INTERSECT service that provides data transformation capabilities for DIAL active learning workflows.

The chart is based on the [Bitnami Charts Template](https://github.com/bitnami/charts) and uses the Bitnami Common library for standardization.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installation

### Add Bitnami Repository (if not already added)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install the Chart

1. Update dependencies:
```bash
cd charts/dial-transformer
helm dependency update
```

2. Install the chart with default values:
```bash
helm install dial-transformer . -n dial-transformer --create-namespace
```

3. Or install with custom values:
```bash
helm install dial-transformer . -n dial-transformer --create-namespace -f values.yaml
```

## Configuration

### Key Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `dialTransformer.image.repository` | Dial Transformer image repository | `intersect-dial/dial-transformer` |
| `dialTransformer.image.tag` | Dial Transformer image tag | `0.1.2` |
| `replicaCount` | Number of replicas | `1` |
| `dialTransformer.configFile` | Configuration file contents (mounted at `/app/local-conf.docker.json`) | See values.yaml |
| `dialTransformer.configFileExistingSecret` | Use an existing secret instead of creating one | `""` |

### INTERSECT Configuration

Configure INTERSECT-specific settings in `values.yaml` via the JSON block under `dialTransformer.configFile`:

```yaml
dialTransformer:
  configFile: |
    {
      "intersect": {
        "brokers": [
          {
            "username": "intersect_username",
            "password": "intersect_password",
            "host": "broker",
            "port": 5672,
            "protocol": "amqp0.9.1"
          }
        ]
      },
      "intersect-hierarchy": {
        "organization": "ornl",
        "facility": "intersect",
        "system": "dial-transformer-system",
        "subsystem": "dial-transformer-subsystem",
        "service": "dial-transformer-service"
      }
    }
```

### Using an Existing Secret

To provide the configuration via a pre-existing Kubernetes secret:

```yaml
dialTransformer:
  configFileExistingSecret: "my-dial-transformer-secret"
```

The secret must contain a key `local-conf.json` with the JSON configuration.

### Diagnostic Mode

To override the container entrypoint for debugging:

```yaml
dialTransformer:
  diagnosticMode:
    enabled: true
    command:
      - sleep
    args:
      - infinity
```

### Resource Limits

```yaml
dialTransformer:
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
```
