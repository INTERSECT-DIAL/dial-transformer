import pytest
from pydantic import ValidationError

from intersect_dial_transformer.data_models import (
    CalculateBoundsParams,
    InitializeTransformParams,
    InverseTransformParams,
    InverseTransformResult,
    TransformParams,
    TransformResult,
)


def test_initialize_transform_params_with_bin_sizes() -> None:
    params = InitializeTransformParams(origins=[0.0, 1.0], bin_sizes=[0.5, 0.25], type='linear')

    assert params.origins == [0.0, 1.0]
    assert params.bin_sizes == [0.5, 0.25]
    assert params.num_bins is None
    assert params.type == 'linear'


def test_initialize_transform_params_with_num_bins() -> None:
    params = InitializeTransformParams(origins=[1.0, 2.0], num_bins=[10, 20], type='logarithmic')

    assert params.origins == [1.0, 2.0]
    assert params.num_bins == [10, 20]
    assert params.bin_sizes is None


def test_initialize_transform_params_rejects_neither_bin_spec_for_linear() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[0.0, 1.0], type='linear')


def test_initialize_transform_params_rejects_num_bins_for_linear() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[0.0, 1.0], num_bins=[10, 20], type='linear')


def test_initialize_transform_params_rejects_both_bin_specs_for_linear() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(
            origins=[0.0, 1.0],
            bin_sizes=[0.5, 0.25],
            num_bins=[10, 20],
            type='linear',
        )


def test_initialize_transform_params_rejects_both_bin_specs_for_logarithmic() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(
            origins=[1.0, 2.0],
            bin_sizes=[0.5, 0.25],
            num_bins=[10, 20],
            type='logarithmic',
        )


def test_initialize_transform_params_rejects_missing_num_bins_for_logarithmic() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[1.0, 2.0], type='logarithmic')


def test_initialize_transform_params_rejects_mismatched_bin_sizes_length() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[0.0, 1.0], bin_sizes=[0.5], type='linear')


def test_initialize_transform_params_rejects_mismatched_num_bins_length() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[1.0, 2.0], num_bins=[10], type='logarithmic')


def test_initialize_transform_params_rejects_non_positive_num_bins() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[1.0, 2.0], num_bins=[10, 0], type='logarithmic')


def test_initialize_transform_params_rejects_invalid_literal() -> None:
    with pytest.raises(ValidationError):
        InitializeTransformParams(origins=[0.0], bin_sizes=[0.5], type='invalid')


def test_calculate_bounds_params_validates_successfully() -> None:
    params = CalculateBoundsParams(
        input_bounds=[[0.0, 1.0], [1.0, 2.0]],
        output_bounds=[[5.0, 10.0]],
        type='linear',
    )

    assert params.input_bounds[0] == [0.0, 1.0]
    assert params.output_bounds[0] == [5.0, 10.0]


def test_calculate_bounds_params_rejects_non_list_bounds() -> None:
    with pytest.raises(ValidationError):
        CalculateBoundsParams(input_bounds='not-a-list', output_bounds=[[1.0, 2.0]], type='linear')


def test_transform_models_validate_successfully() -> None:
    params = TransformParams(values=[1.0, 2.0])
    result = TransformResult(transformed_values=[[4.0, 5.0], [6.0, 7.0]])

    assert params.values == [1.0, 2.0]
    assert result.transformed_values == [[4.0, 5.0], [6.0, 7.0]]


def test_transform_models_reject_invalid_next_x() -> None:
    with pytest.raises(ValidationError):
        TransformParams(values=['x'])


def test_inverse_transform_models_validate_successfully() -> None:
    params = InverseTransformParams(transformed_values=[7.0, 8.0])
    result = InverseTransformResult(values=[9.0, 10.0], score=0.8)

    assert params.transformed_values == [7.0, 8.0]
    assert result.values == [9.0, 10.0]
    assert result.score == 0.8


def test_inverse_transform_models_reject_empty_next_x() -> None:
    with pytest.raises(ValidationError):
        InverseTransformParams(transformed_values=[])
