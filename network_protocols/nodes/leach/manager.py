import random
from network_protocols.nodes.base import BaseLeachNode, BaseLeachStation, BaseNodeProps
from network_protocols.settings.config import Config


class ClusterManager:
    def __init__(self, width: int = Config.SCREEN_WIDTH, height: int = Config.SCREEN_HEIGHT) -> None:
        self._screen_width: int = width
        self._screen_height: int = height
        self._nodes_by_clusters: dict = {
            1: [],
            2: [],
            3: [],
            4: [],
        }
        self._clusters_state: dict[int, set] = {
            1: set(),
            2: set(),
            3: set(),
            4: set(),
        }

    def find_cluster_heads(self) -> None:
        """Find a new cluster heads by the cluster state"""
        for cluster_id, cluster_nodes in self._clusters_state.items():
            if len(cluster_nodes) <= 0:
                self._clusters_state[cluster_id] = set(self._nodes_by_clusters[cluster_id])

        for cluster_id, cluster_nodes in self._clusters_state.items():
            if len(cluster_nodes) > 0:
                random_node = random.choice(list(cluster_nodes))

                if random_node.is_cluster_head or random_node._energy <= 0:
                    continue

                self._clusters_state[cluster_id].remove(random_node)

                random_node.is_cluster_head = True

    def initialize_clusters_state(self, nodes: list[BaseNodeProps]) -> None:
        """Initnialize clusters state. Before initnialization, nodes will be clear"""
        for node in nodes:
            if isinstance(node, BaseLeachStation):
                continue

            if 0 <= node.coordinates[0] <= self._screen_width // 2:
                if 0 <= node.coordinates[1] <= self._screen_height // 2:
                    self._nodes_by_clusters[1].append(node)
                else:
                    self._nodes_by_clusters[2].append(node)
            else:
                if 0 <= node.coordinates[1] <= self._screen_height // 2:
                    self._nodes_by_clusters[3].append(node)
                else:
                    self._nodes_by_clusters[4].append(node)

    def get_cluster_id_by_node(self, node: BaseLeachNode) -> int:
        """Returns the cluster_id by the node"""
        if isinstance(node, BaseLeachStation):
            return 0

        for cluster_id, nodes in self._nodes_by_clusters.items():
            if node in nodes:
                return cluster_id

    def get_nodes_by_cluster_index(self, cluster_index: int) -> list[BaseLeachNode]:
        """Returns the nodes by the cluster index"""
        return self._nodes_by_clusters[cluster_index]
