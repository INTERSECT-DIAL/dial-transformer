# DIAL Transformer

## API

Everything here is an `@intersect_message`

- `initialize_transform(origins: list[float], bin_sizes: list[float], type: Literal['linear']) -> None`
- `calculate_bounds(input_bounds: list[list[float]], output_bounds: list[list[float]]) -> None`
- `transform(next_x: list[float], next_y: float) -> tuple[list[float], float]`
- `inverse_transform(next_x: list[float], next_y: float) -> tuple[list[float], float]`
