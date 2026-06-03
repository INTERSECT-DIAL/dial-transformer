"""INTERSECT Capability definitions."""

from intersect_sdk import (
    IntersectBaseCapabilityImplementation,
    intersect_message,
)

from .data_models import (
    CalculateBoundsParams,
    InitializeTransformParams,
    InverseTransformParams,
    InverseTransformResult,
    TransformParams,
    TransformResult,
)
from .transformer import Transformer


class DialTransformerCapability(IntersectBaseCapabilityImplementation):
    """Main INTERSECT entrypoint."""

    intersect_sdk_capability_name = 'dial_transformer'

    def __init__(self) -> None:
        self._transformer: Transformer | None = None

    @intersect_message
    def initialize_transform(self, params: InitializeTransformParams) -> None:
        self._transformer = Transformer(params)

    @intersect_message
    def calculate_bounds(self, params: CalculateBoundsParams) -> None:
        transformer = self._require_initialized_transformer()
        params.output_bounds = transformer.calculate_bounds(params.input_bounds, params.type)

    @intersect_message
    def transform(self, params: TransformParams) -> TransformResult:
        transformer = self._require_initialized_transformer()
        transformed_values = transformer.transform(params.values)
        return TransformResult(transformed_values=[transformed_values])

    @intersect_message
    def inverse_transform(self, params: InverseTransformParams) -> InverseTransformResult:
        transformer = self._require_initialized_transformer()
        values = transformer.inverse_transform(params.transformed_values)
        return InverseTransformResult(values=values, score=1.0)

    def _require_initialized_transformer(self) -> Transformer:
        if self._transformer is None:
            msg = 'Transformer has not been initialized. Call initialize_transform first.'
            raise RuntimeError(msg)
        return self._transformer
