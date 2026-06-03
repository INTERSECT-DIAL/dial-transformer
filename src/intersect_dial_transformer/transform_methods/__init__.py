"""Transform method implementations and registries by transform type."""

from collections.abc import Callable

from .linear import linear_inverse_transform, linear_transform
from .logarithmic import logarithmic_inverse_transform, logarithmic_transform

TransformMethod = Callable[[list[float], list[float], list[float]], list[float]]

TRANSFORM_METHODS: dict[str, TransformMethod] = {
    'linear': linear_transform,
    'logarithmic': logarithmic_transform,
}

INVERSE_TRANSFORM_METHODS: dict[str, TransformMethod] = {
    'linear': linear_inverse_transform,
    'logarithmic': logarithmic_inverse_transform,
}
