from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from network_protocols.buffers.base import BaseBuffer
from network_protocols.buffers.queue import Queue
from network_protocols.settings.config import Config


class BaseNodeProps(ABC):
    def __init__(self, pos_x: int, pos_y: int, radius: int = Config.NODE_RADIUS) -> None:
        self._oid: UUID = uuid4()
        self._pos_x: int = pos_x
        self._pos_y: int = pos_y
        self._speed: int = Config.NODE_SPEED
        self._energy: int = Config.NODE_ENERGY
        self._radius: int = radius * self._energy
        self._neighbors: list["BaseNodeProps"] = list()
        self._buffer: BaseBuffer = Queue()

    @property
    def oid(self) -> UUID:
        """Returns the unique id of the current node"""
        return self._oid

    @property
    def neighbors(self) -> list["BaseNodeProps"]:
        """Returns the neighbors of the current node"""
        return self._neighbors

    @property
    def buffer(self) -> BaseBuffer:
        """Returns the buffer of the current node"""
        return self._buffer

    @property
    def coordinates(self) -> tuple[int, int]:
        """Returns the coordinates of the current node"""
        return self._pos_x, self._pos_y

    @abstractmethod
    def find_neighbors(self, nodes: list["BaseNodeProps"]) -> None:
        ...


class BaseFloodNode(BaseNodeProps):
    @abstractmethod
    def change_position(self, max_x: int, max_y: int) -> None:
        ...

    @abstractmethod
    def send_messages(self, fpr: int) -> None:
        ...


class BaseFloodGateway(BaseNodeProps):
    @abstractmethod
    def clear_buffer(self) -> None:
        ...


class BaseLeachNode(BaseNodeProps):
    def __init__(self, pos_x: int, pos_y: int, radius: int = Config.NODE_RADIUS) -> None:
        super().__init__(pos_x, pos_y, radius)
        self._is_cluster_head: bool = False

    @property
    def is_cluster_head(self) -> bool:
        """Returns True if the current node is cluster head. Else returns False"""
        return self._is_cluster_head

    @is_cluster_head.setter
    def is_cluster_head(self, value: bool) -> None:
        self._is_cluster_head = value

    @abstractmethod
    def change_position(self, max_x: int, max_y: int) -> None:
        ...

    @abstractmethod
    def receive_messages(self) -> None:
        ...


class BaseLeachStation(BaseNodeProps):
    @abstractmethod
    def receive_messages(self) -> None:
        ...

    @abstractmethod
    def clear_buffer(self) -> None:
        ...


# TODO: add methods for funnel station
class BaseFunnelStation(BaseNodeProps):
    ...


class BaseFunnelNode(BaseNodeProps):
    ...
