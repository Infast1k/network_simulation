from network_protocols.nodes.base import BaseFloodGateway, BaseNodeProps


class FloodGateway(BaseFloodGateway):
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

    def clear_buffer(self) -> None:
        """Clears the buffer"""
        self.buffer.clear()
