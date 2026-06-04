# Helm Charts

This GitHub Pages site hosts Helm charts published from the
[dial-transformer repository](https://github.com/INTERSECT-DIAL/dial-transformer).

## Usage

[Helm](https://helm.sh/) must be installed first.

Add the chart repository:

```bash
helm repo add intersect-dial-transformer https://intersect-dial.github.io/dial-transformer
```

If you already added it before, refresh chart metadata:

```bash
helm repo update
```

List available charts:

```bash
helm search repo intersect-dial-transformer
```

## Available Charts

- `dial-transformer`

## Install

```bash
helm install dial-transformer intersect-dial-transformer/dial-transformer \
  --namespace intersect \
  --create-namespace
```

## Upgrade

```bash
helm upgrade dial-transformer intersect-dial-transformer/dial-transformer \
  --namespace intersect
```

## Uninstall

```bash
helm uninstall dial-transformer --namespace intersect
```
