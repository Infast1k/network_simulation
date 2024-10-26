import logging

from network_protocols.nodes.base import BaseLeachNode, BaseLeachStation
from network_protocols.settings.config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class LeachStation(BaseLeachStation):
    def clear_buffer(self) -> None:
        """Delete all packets from the buffer"""
        self.buffer.clear()

    def receive_messages(self, fpr: int = 5) -> None:
        """Receive messages from the cluster head nodes"""
        for node in self._neighbors:
            if isinstance(node, BaseLeachStation):
                continue

            for _ in range(fpr):
                message = node.buffer.pop()
                if message is None:
                    break

                self.buffer.put(message)

            logger.info("Buffer length for node %s: %s\n", node.oid, node.buffer.length)

        self.buffer.clear()

    def find_neighbors(self, nodes: list[BaseLeachNode]) -> None:
        """Find each cluster head nodes"""
        if len(self.neighbors) > 0:
            self.neighbors.clear()

        for node in nodes:
            if isinstance(node, BaseLeachNode) and node.is_cluster_head:
                self.neighbors.append(node)
