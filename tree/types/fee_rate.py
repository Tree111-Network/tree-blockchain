from __future__ import annotations

import math
from dataclasses import dataclass

import typing_extensions

from tree.types.clvm_cost import CLVMCost
from tree.types.mojos import Mojos
from tree.util.ints import uint64
from tree.util.streamable import Streamable, streamable


@typing_extensions.final
@streamable
@dataclass(frozen=True)
class FeeRate(Streamable):
    """
    Represents Fee Rate in mojos divided by CLVM Cost.
    Performs TREE111/mojo conversion.
    Similar to 'Fee per cost'.
    """

    mojos_per_clvm_cost: uint64

    @classmethod
    def create(cls, mojos: Mojos, clvm_cost: CLVMCost) -> FeeRate:
        return cls(uint64(math.ceil(mojos / clvm_cost)))
