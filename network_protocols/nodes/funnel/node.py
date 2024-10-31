import math
import random
from typing import Optional

from network_protocols.nodes.base import BaseFunnelNode, BaseFunnelStation, BaseNodeProps
from network_protocols.settings.config import Config


class FunnelNode(BaseFunnelNode):
    def send_messages(self, fpr: int) -> None:
        """
        Sends the messages to the neighbors if has at least one neighbor.
        Fpr is the constraint for the number of messages per round.
        """
        if self.buffer.length == 0 or len(self._neighbors) == 0:
            return

        receiver = self._nearest_neighbor_to_station(neighbors=self._neighbors)

        if receiver is None:
            return

        for _ in range(fpr):
            message = self.buffer.pop()
            if message is None:
                break

            receiver.buffer.put(data=message)

    def _nearest_neighbor_to_station(self, neighbors: list[BaseNodeProps]) -> Optional[BaseNodeProps]:
        """
        Finds the nearest neighbor to the station.
        If nearest neighbor is a current node, returns None.
        Station is the center of the screen.
        """
        nearest_node = None
        nearest_distance = float("inf")

        for neighbor in neighbors:
            if isinstance(neighbor, BaseFunnelStation):
                return neighbor

            neighobr_distance = math.sqrt(
                (neighbor.coordinates[0] - Config.SCREEN_WIDTH / 2) ** 2
                + (neighbor.coordinates[1] - Config.SCREEN_HEIGHT / 2) ** 2
            )

            if neighobr_distance < nearest_distance:
                nearest_distance = neighobr_distance
                nearest_node = neighbor

        return nearest_node

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

            if (x - center_x) ** 2 + (y - center_y) ** 2 <= self._radius ** 2:
                self._neighbors.append(neighbor)

    def change_position(self, max_x: int, max_y: int) -> None:
        """Changes the position of the current node. Energy is decreased by 0.1 on each move."""
        self._energy -= 0.005

        if self._energy <= 0:
            self._energy = 0
            return

        self._radius = self._energy * Config.NODE_RADIUS

        if self.coordinates[0] < Config.SCREEN_WIDTH // 2:
            self._pos_x += random.randint(-self._speed + 5, self._speed)
        else:
            self._pos_x += random.randint(-self._speed, self._speed - 5)

        if self.coordinates[1] < Config.SCREEN_HEIGHT // 2:
            self._pos_y += random.randint(-self._speed, self._speed + 5)
        else:
            self._pos_y += random.randint(-self._speed - 5, self._speed)

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
