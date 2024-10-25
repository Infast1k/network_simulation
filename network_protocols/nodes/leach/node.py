import logging
import random

from network_protocols.nodes.base import BaseLeachNode, BaseNodeProps
from network_protocols.settings.config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class LeachNode(BaseLeachNode):
    def find_neighbors(self, nodes: list[BaseNodeProps]) -> None:
        if not self._is_cluster_head:
            return

        for node in nodes:
            if isinstance(node, LeachNode) and not node.is_cluster_head:
                self.neighbors.append(node)

    def receive_messages(self, nodes: list[BaseNodeProps], fpr: int = 5) -> None:
        """Method which receives messages from the base nodes"""
        if not self._is_cluster_head:
            return

        for neighbor in nodes:
            for _ in range(fpr):
                message = neighbor.buffer.pop()
                if message is None:
                    logger.info("Buffer is empty for node %s", neighbor.oid)
                    break

                self.buffer.put(message)

        logger.info("Buffer length for cluster head %s after receiving: %s\n", self.oid, self.buffer.length)

    def change_position(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        """Changes the position of the current node. Energy is decreased by 0.1 on each move."""
        self._energy -= 0.01
        self._neighbors.clear()
        self._is_cluster_head = False

        if self._energy <= 0:
            self._energy = 0
            return

        self._radius = self._energy * Config.NODE_RADIUS

        self._pos_x += random.randint(-self._speed, self._speed)
        self._pos_y += random.randint(-self._speed, self._speed)

        self._validate_new_position(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)

    def _validate_new_position(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        """Validates the new position of the current node"""
        if self._pos_x < min_x:
            self._pos_x = min_x
        elif self._pos_x > max_x:
            self._pos_x = max_x

        if self._pos_y < min_y:
            self._pos_y = min_y
        elif self._pos_y > max_y:
            self._pos_y = max_y
