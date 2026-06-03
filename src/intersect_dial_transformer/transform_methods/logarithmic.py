"""Logarithmic transform method implementations."""

import math


def logarithmic_transform(
    values: list[float],
    origins: list[float],
    num_bins: list[float],
) -> list[float]:
    """Apply logarithmic transform using bin-count-driven geometric spacing.

    For each dimension, define ratio r = exp(1 / num_bins). Then:
    y = origin * r ** x

    The local bin size is variable and can be derived during transform as:
    delta_y = y * (r - 1)
    """
    transformed_values: list[float] = []
    for value, origin, bins in zip(values, origins, num_bins, strict=True):
        if origin <= 0:
            msg = 'Logarithmic transform requires origins > 0 for all dimensions'
            raise ValueError(msg)
        if bins <= 0:
            msg = 'Logarithmic transform requires num_bins > 0 for all dimensions'
            raise ValueError(msg)
        ratio = math.exp(1.0 / bins)
        transformed_values.append(origin * (ratio**value))
    return transformed_values


def logarithmic_inverse_transform(
    transformed_values: list[float],
    origins: list[float],
    num_bins: list[float],
) -> list[float]:
    """Invert logarithmic transform using configured per-dimension num_bins."""
    values: list[float] = []
    for transformed_value, origin, bins in zip(
        transformed_values,
        origins,
        num_bins,
        strict=True,
    ):
        if origin <= 0:
            msg = 'Logarithmic inverse transform requires origins > 0 for all dimensions'
            raise ValueError(msg)
        if transformed_value <= 0:
            msg = 'Logarithmic inverse transform requires transformed values > 0'
            raise ValueError(msg)
        if bins <= 0:
            msg = 'Logarithmic inverse transform requires num_bins > 0 for all dimensions'
            raise ValueError(msg)
        ratio = math.exp(1.0 / bins)
        values.append(math.log(transformed_value / origin) / math.log(ratio))
    return values
