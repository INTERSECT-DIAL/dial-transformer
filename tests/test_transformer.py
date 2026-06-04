import pytest

from intersect_dial_transformer.capability import DialTransformerCapability
from intersect_dial_transformer.data_models import (
    CalculateBoundsParams,
    InitializeTransformParams,
    InverseTransformParams,
    TransformParams,
)
from intersect_dial_transformer.transformer import Transformer


def test_linear_transform_applies_expected_formula() -> None:
    params = InitializeTransformParams(origins=[10.0, -3.0], bin_sizes=[2.0, 0.5], type='linear')
    transformer = Transformer(params)

    transformed = transformer.transform([4.0, 8.0])

    assert transformed == [18.0, 1.0]


def test_linear_inverse_transform_round_trip_recovers_inputs() -> None:
    params = InitializeTransformParams(origins=[1.0, -10.0, 5.5], bin_sizes=[2.0, 4.0, 0.25], type='linear')
    transformer = Transformer(params)
    original_values = [7.0, 2.0, -3.0]

    transformed = transformer.transform(original_values)
    recovered = transformer.inverse_transform(transformed)

    assert recovered == pytest.approx(original_values)


def test_transform_rejects_dimension_mismatch() -> None:
    params = InitializeTransformParams(origins=[1.0, 2.0], bin_sizes=[3.0, 4.0], type='linear')
    transformer = Transformer(params)

    with pytest.raises(ValueError, match='Input values length must match'):
        transformer.transform([10.0])


def test_logarithmic_transform_round_trip_recovers_inputs() -> None:
    params = InitializeTransformParams(
        origins=[1.0, 2.5],
        num_bins=[12, 20],
        type='logarithmic',
    )
    transformer = Transformer(params)
    original_values = [2.0, 5.0]

    transformed = transformer.transform(original_values)
    recovered = transformer.inverse_transform(transformed)

    assert recovered == pytest.approx(original_values)


def test_logarithmic_transform_rejects_non_positive_origins() -> None:
    params = InitializeTransformParams(origins=[0.0], num_bins=[10], type='logarithmic')
    transformer = Transformer(params)

    with pytest.raises(ValueError, match='origins > 0'):
        transformer.transform([1.0])


def test_logarithmic_inverse_transform_rejects_non_positive_transformed_values() -> None:
    params = InitializeTransformParams(origins=[1.0], num_bins=[10], type='logarithmic')
    transformer = Transformer(params)

    with pytest.raises(ValueError, match='transformed values > 0'):
        transformer.inverse_transform([0.0])


def test_capability_initializes_and_uses_transformer() -> None:
    capability = DialTransformerCapability()
    init_params = InitializeTransformParams(origins=[2.0, 1.0], bin_sizes=[4.0, 0.5], type='linear')

    capability.initialize_transform(init_params)
    transformed = capability.transform(TransformParams(values=[3.0, 8.0]))
    inverse = capability.inverse_transform(InverseTransformParams(transformed_values=[14.0, 5.0]))

    assert transformed.transformed_values == [14.0, 5.0]
    assert inverse.values == pytest.approx([3.0, 8.0])
    assert inverse.labx == pytest.approx(3.0)
    assert inverse.labz == pytest.approx(8.0)
    assert inverse.score == 1.0


def test_capability_requires_initialization() -> None:
    capability = DialTransformerCapability()

    with pytest.raises(RuntimeError, match='initialize_transform'):
        capability.transform(TransformParams(values=[1.0]))


def test_capability_calculate_bounds_with_linear_bin_sizes() -> None:
    capability = DialTransformerCapability()
    init_params = InitializeTransformParams(origins=[0.0, 0.0], bin_sizes=[2.0, 5.0], type='linear')
    bounds_params = CalculateBoundsParams(
        input_bounds=[[10.0, 30.0], [100.0, 130.0]],
        output_bounds=[[0.0, 0.0], [0.0, 0.0]],
        type='linear',
    )

    capability.initialize_transform(init_params)
    capability.calculate_bounds(bounds_params)

    assert bounds_params.output_bounds == [[0.0, 10.0], [0.0, 6.0]]


def test_capability_calculate_bounds_linear_from_num_bins_on_log_transformer() -> None:
    capability = DialTransformerCapability()
    init_params = InitializeTransformParams(origins=[1.0, 2.0], num_bins=[10, 6], type='logarithmic')
    bounds_params = CalculateBoundsParams(
        input_bounds=[[10.0, 30.0], [100.0, 130.0]],
        output_bounds=[[0.0, 0.0], [0.0, 0.0]],
        type='linear',
    )

    capability.initialize_transform(init_params)
    capability.calculate_bounds(bounds_params)

    assert bounds_params.output_bounds == [[0.0, 10.0], [0.0, 6.0]]