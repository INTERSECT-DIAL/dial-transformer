# DIAL Transformer

## Overview

DIAL Transformer is an INTERSECT capability service that applies configurable data transforms
for DIAL workflows. It currently supports linear and logarithmic transforms, and includes a
linear bounds-calculation path for generating regular grid-style bounds from incoming bounding boxes.

## Developer Setup (uv)

1. Install uv.
2. Sync dependencies:

```bash
uv sync
```

3. Run tests:

```bash
uv run pytest -q
```

4. Run the service:

```bash
uv run python -m intersect_dial_transformer --config local-conf.json
```

## Docker

Build the image and run directly:

```bash
docker build -t dial-transformer . && docker run -e DIAL_TRANSFORMER_CONFIG_FILE=/local-conf.docker.json -v ${PWD}/local-conf.docker.json:/local-conf.docker.json dial-transformer
```

Run with Compose:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up --build -d
```

Stop and clean up:

```bash
docker compose down
```

Notes:
- The service image is built from Dockerfile.
- The container should set `DIAL_TRANSFORMER_CONFIG_FILE=/local-conf.docker.json`.
- Compose mounts `./local-conf.docker.json` to `/local-conf.docker.json`.

## API

Everything here is an @intersect_message.

- initialize_transform(params: InitializeTransformParams) -> None
- calculate_bounds(params: CalculateBoundsParams) -> list[list[float]]
- transform(params: TransformParams) -> TransformResult
- inverse_transform(params: InverseTransformParams) -> InverseTransformResult

### Payload Notes

- InitializeTransformParams
  - origins: list[float]
  - type: 'linear' | 'logarithmic'
  - linear requires bin_sizes
  - logarithmic requires num_bins
- CalculateBoundsParams
  - input_bounds: list[[min, max]] per dimension
  - output_bounds: list[[min, max]] per dimension (updated by service)
  - type: 'linear'
