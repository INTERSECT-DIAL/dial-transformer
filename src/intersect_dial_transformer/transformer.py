"""Stateful transformer for applying initialized transform behavior."""

from .data_models import InitializeTransformParams
from .transform_methods import INVERSE_TRANSFORM_METHODS, TRANSFORM_METHODS, TransformMethod


class Transformer:
    """Transformer configured from initialize_transform input parameters."""

    def __init__(self, params: InitializeTransformParams) -> None:
        self.origins = params.origins
        self.type = params.type
        self.bin_sizes = params.bin_sizes
        self.num_bins = params.num_bins
        self.bin_parameters = self._get_bin_parameters(params)
        self._transform_method = self._get_method(TRANSFORM_METHODS)
        self._inverse_transform_method = self._get_method(INVERSE_TRANSFORM_METHODS)

    def _get_bin_parameters(self, params: InitializeTransformParams) -> list[float]:
        if params.type == 'linear':
            if params.bin_sizes is None:
                msg = 'linear transform requires bin_sizes to be initialized'
                raise ValueError(msg)
            return params.bin_sizes
        if params.type == 'logarithmic':
            if params.num_bins is None:
                msg = 'logarithmic transform requires num_bins to be initialized'
                raise ValueError(msg)
            return [float(value) for value in params.num_bins]

        msg = f'Unsupported transform type: {params.type}'
        raise ValueError(msg)

    def calculate_bounds(self, input_bounds: list[list[float]], bounds_type: str) -> list[list[float]]:
        """Compute normalized grid-aligned bounds from an incoming bounding box."""
        self._validate_input_length(input_bounds)

        if bounds_type == 'linear':
            return self._calculate_linear_bounds(input_bounds)

        msg = f'calculate_bounds is not implemented for type: {bounds_type}'
        raise NotImplementedError(msg)

    def _calculate_linear_bounds(self, input_bounds: list[list[float]]) -> list[list[float]]:
        resolved_bin_sizes = self._resolve_linear_bin_sizes(input_bounds)
        output_bounds: list[list[float]] = []
        for bound, bin_size in zip(input_bounds, resolved_bin_sizes, strict=True):
            min_bound, max_bound = self._validate_bound_pair(bound)
            span = max_bound - min_bound
            output_bounds.append([0.0, span / bin_size])
        return output_bounds

    def _resolve_linear_bin_sizes(self, input_bounds: list[list[float]]) -> list[float]:
        if self.bin_sizes is not None:
            if len(self.bin_sizes) != len(input_bounds):
                msg = 'Configured bin_sizes length must match bounds dimensions'
                raise ValueError(msg)
            if any(bin_size <= 0 for bin_size in self.bin_sizes):
                msg = 'Configured bin_sizes values must all be > 0'
                raise ValueError(msg)
            return self.bin_sizes

        if self.num_bins is None:
            msg = 'linear bounds calculation requires bin_sizes or num_bins'
            raise ValueError(msg)

        resolved: list[float] = []
        for bound, num_bins in zip(input_bounds, self.num_bins, strict=True):
            min_bound, max_bound = self._validate_bound_pair(bound)
            if num_bins <= 0:
                msg = 'num_bins values must all be > 0'
                raise ValueError(msg)
            span = max_bound - min_bound
            resolved.append(span / float(num_bins))
        return resolved

    def _validate_bound_pair(self, bound: list[float]) -> tuple[float, float]:
        if len(bound) != 2:
            msg = 'Each bounds entry must contain exactly [min, max]'
            raise ValueError(msg)
        min_bound, max_bound = bound
        if max_bound <= min_bound:
            msg = 'Each bounds pair must satisfy max > min'
            raise ValueError(msg)
        return min_bound, max_bound

    def _get_method(self, registry: dict[str, TransformMethod]) -> TransformMethod:
        try:
            return registry[self.type]
        except KeyError as exc:
            msg = f'Unsupported transform type: {self.type}'
            raise ValueError(msg) from exc

    def transform(self, values: list[float]) -> list[float]:
        """Run configured forward transform over input values."""
        self._validate_input_length(values)
        return self._transform_method(values, self.origins, self.bin_parameters)

    def inverse_transform(self, transformed_values: list[float]) -> list[float]:
        """Run configured inverse transform over transformed values."""
        self._validate_input_length(transformed_values)
        return self._inverse_transform_method(
            transformed_values,
            self.origins,
            self.bin_parameters,
        )

    def _validate_input_length(self, values: list[float] | list[list[float]]) -> None:
        if len(values) != len(self.origins):
            msg = 'Input values length must match initialized origins length'
            raise ValueError(msg)