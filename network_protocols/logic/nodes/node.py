import logging
import random

from network_protocols.logic.nodes.base import BaseNode, BaseNodeProps
from network_protocols.settings.config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Node(BaseNode):
    def send_messages(self, fpr: int = 5) -> None:
        """Sends the messages to the neighbors. Fpr is the constraint for the number of messages per round."""
        for _ in range(fpr):
            if not len(self.neighbors):
                break

            message = self.buffer.pop()
            if message is None:
                break

            for neighbor in self.neighbors:
                if neighbor.oid != message.packet.owner_oid:
                    neighbor.buffer.put(message)

        logger.info("Buffer length for node %s after sending: %s\n", self.oid, self.buffer.length)

    def find_neighbors(self, nodes: list[BaseNodeProps]) -> None:
        """
        Finds the neighbors of the current node.
        Before finding neighbors, it clears the list of neighbors.
        """
        if len(self._neighbors) > 0:
            self._neighbors.clear()

        center_x, center_y = self.coordinates

        for neighbor in nodes:
            if neighbor.oid == self.oid:
                continue

            x, y = neighbor.coordinates

            # NOTE: Formula for finding points in the circle radius:
            # (x - center_x)² + (y - center_y)² = radius²
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= self._radius ** 2:
                self._neighbors.append(neighbor)

    def change_position(self, max_x: int, max_y: int) -> None:
        """Changes the position of the current node. Energy is decreased by 0.1 on each move."""
        self._energy -= 0.01

        if self._energy <= 0:
            self._energy = 0

        self._radius = self._energy * Config.NODE_RADIUS

        self._pos_x += random.randint(-self._speed, self._speed)
        self._pos_y += random.randint(-self._speed, self._speed)

        self._validate_new_position(max_x=max_x, max_y=max_y)

    def _validate_new_position(self, max_x: int, max_y: int) -> None:
        """Validates the new position of the current node"""
        if self._pos_x < 0:
            self._pos_x = 0
        elif self._pos_x > max_x:
            self._pos_x = max_x

        if self._pos_y < 0:
            self._pos_y = 0
        elif self._pos_y > max_y:
            self._pos_y = max_y
