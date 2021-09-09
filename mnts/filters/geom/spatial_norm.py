import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple
from ..mnts_filters import MNTSFilter


__all__ = ['SpatialNorm']

class SpatialNorm(MNTSFilter):
    r"""
    This class utilize the SimpleITK filter `ResampleImageFilter` to change the spacing. All other factors remains
    unchanged. However, note that the floating point rounding might results in slightly different image dimension, so
    this filter should be used with the cropping filter if you require uniform data size.

    Attributes:
        out_spacing (float, tuple of floats):
            Desired uniform spacing. Unit is mm. Use 0 or negative values if spacing is to be kept

    """
    def __init__(self, out_spacing: Union[float, Tuple[float, float, float]] = None):
        super(SpatialNorm, self).__init__()
        self.out_spacing = out_spacing

    @property
    def out_spacing(self):
        return self._out_spacing

    @out_spacing.setter
    def out_spacing(self, out_spacing: Union[float, Tuple[float, float, float]]):
        self._out_spacing = out_spacing if isinstance(out_spacing, (list, tuple)) else [out_spacing]*3


    def filter(self, input: sitk.Image):
        original_size = np.asarray(input.GetSize())
        original_spacing = np.asarray(input.GetSpacing())

        # Keep spacing if there's a negative value in out_spacing
        new_spacing = np.asarray(self.out_spacing)
        new_spacing[new_spacing <= 0] = original_spacing[new_spacing <=0]

        new_size = np.floor((original_size * original_spacing) / new_spacing).astype('int').tolist()
        self._logger.info(f"From {original_size} -> {new_size}")

        f = sitk.ResampleImageFilter()
        f.SetReferenceImage(input)
        f.SetOutputSpacing(new_spacing.tolist())
        f.SetSize(new_size)
        return f.Execute(input)

