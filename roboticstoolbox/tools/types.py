#!/usr/bin/env python
"""
@author Jesse Haviland
"""

from collections.abc import Sequence, Set
from typing import Any, TypeAlias
import numpy.typing as npt

NDArray: TypeAlias = npt.NDArray[Any]

PyArrayLike: TypeAlias = Sequence[float] | Set[float]

ArrayLike: TypeAlias = npt.ArrayLike | Set[float]
