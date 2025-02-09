from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, SupportsBytes, Union

from tree.protocols.protocol_message_types import ProtocolMessageTypes
from tree.util.ints import uint8, uint16
from tree.util.streamable import Streamable, streamable


class NodeType(IntEnum):
    FULL_NODE = 1
    HARVESTER = 2
    FARMER = 3
    TIMELORD = 4
    INTRODUCER = 5
    WALLET = 6
    DATA_LAYER = 7


@streamable
@dataclass(frozen=True)
class Message(Streamable):
    type: uint8  # one of ProtocolMessageTypes
    # message id
    id: Optional[uint16]
    # Message data for that type
    data: bytes


def make_msg(msg_type: ProtocolMessageTypes, data: Union[bytes, SupportsBytes]) -> Message:
    return Message(uint8(msg_type.value), None, bytes(data))
