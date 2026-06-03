"""Linear transform method implementations."""


def linear_transform(values: list[float], origins: list[float], bin_sizes: list[float]) -> list[float]:
    """Apply y_i = bin_size[i] * x_i + origins[i] for each feature dimension."""
    return [
        (bin_size * value) + origin
        for value, origin, bin_size in zip(values, origins, bin_sizes, strict=True)
    ]


def linear_inverse_transform(
    transformed_values: list[float],
    origins: list[float],
    bin_sizes: list[float],
) -> list[float]:
    """Apply x_i = y_i / bin_size[i] - origins[i] / bin_size[i] for each dimension."""
    return [
        (transformed_value / bin_size) - (origin / bin_size)
        for transformed_value, origin, bin_size in zip(
            transformed_values,
            origins,
            bin_sizes,
            strict=True,
        )
    ]
