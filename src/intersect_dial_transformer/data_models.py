"""Pydantic models used by DIAL transformer capability methods."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


class InitializeTransformParams(BaseModel):
    """Input payload for initialize_transform."""

    origins: Annotated[
        list[float],
        Field(min_length=1, description='Vector origin per feature dimension.'),
    ]
    bin_sizes: Annotated[
        list[float] | None,
        Field(default=None, min_length=1, description='Bin size per feature dimension.'),
    ] = None
    num_bins: Annotated[
        list[int] | None,
        Field(default=None, min_length=1, description='Number of bins per feature dimension.'),
    ] = None
    type: Literal['linear', 'logarithmic']

    @model_validator(mode='after')
    def validate_bin_specification(self) -> 'InitializeTransformParams':
        if self.type == 'linear':
            if self.bin_sizes is None:
                msg = 'linear transform requires bin_sizes'
                raise ValueError(msg)
            if self.num_bins is not None:
                msg = 'linear transform does not accept num_bins'
                raise ValueError(msg)
        elif self.type == 'logarithmic':
            if self.num_bins is None:
                msg = 'logarithmic transform requires num_bins'
                raise ValueError(msg)
            if self.bin_sizes is not None:
                msg = 'logarithmic transform does not accept bin_sizes'
                raise ValueError(msg)

        n_dims = len(self.origins)
        if self.bin_sizes is not None and len(self.bin_sizes) != n_dims:
            msg = 'bin_sizes must have the same length as origins'
            raise ValueError(msg)
        if self.num_bins is not None and len(self.num_bins) != n_dims:
            msg = 'num_bins must have the same length as origins'
            raise ValueError(msg)
        if self.num_bins is not None and any(value <= 0 for value in self.num_bins):
            msg = 'num_bins values must all be > 0'
            raise ValueError(msg)
        return self


class CalculateBoundsParams(BaseModel):
    """Input payload for calculate_bounds."""

    input_bounds: Annotated[
        list[list[float]],
        Field(min_length=1, description='Input-space bounds vectors.'),
    ]
    output_bounds: Annotated[
        list[list[float]],
        Field(min_length=1, description='Output-space bounds vectors.'),
    ]
    type: Literal['linear']


class TransformParams(BaseModel):
    """Input payload for transform."""

    values: Annotated[
        list[float] | None,
        Field(min_length=1, description='Values to transform.'),
    ] = None
    labx: float | None = Field(default=None, description='Optional x coordinate input.')
    labz: float | None = Field(default=None, description='Optional z coordinate input.')

    @model_validator(mode='after')
    def validate_values_or_coordinates(self) -> 'TransformParams':
        if self.values is not None:
            return self
        if self.labx is None or self.labz is None:
            msg = 'transform requires either values or both labx and labz'
            raise ValueError(msg)
        self.values = [self.labx, self.labz]
        return self


class TransformResult(BaseModel):
    """Output payload from transform."""

    transformed_values: Annotated[
        list[float],
        Field(min_length=1, description='Transformed values vector.'),
    ]


class InverseTransformParams(BaseModel):
    """Input payload for inverse_transform."""

    transformed_values: Annotated[
        list[float],
        Field(min_length=1, description='Flattened transformed values.'),
    ]


class InverseTransformResult(BaseModel):
    """Output payload from inverse_transform."""

    values: Annotated[
        list[float],
        Field(min_length=1, description='Recovered source values.'),
    ]
    labx: float
    labz: float
    score: float
