from network_protocols.nodes.base import BaseLeachNode, BaseLeachStation, BaseNodeProps
from network_protocols.settings.config import Config


class ClusterManager:
    def __init__(self, width: int = Config.SCREEN_WIDTH, height: int = Config.SCREEN_HEIGHT) -> None:
        self.__screen_width: int = width
        self.__screen_height: int = height
        self.__clusters_state: dict = {
            1: [],
            2: [],
            3: [],
            4: [],
        }

    def initialize_clusters_state(self, nodes: list[BaseNodeProps]) -> None:
        """Initnialize clusters state. Before initnialization, nodes will be clear"""
        for cluster_nodes in self.__clusters_state.values():
            cluster_nodes.clear()

        for node in nodes:
            if isinstance(node, BaseLeachStation):
                continue

            if 0 <= node.coordinates[0] <= self.__screen_width // 2:
                if 0 <= node.coordinates[1] <= self.__screen_height // 2:
                    self.__clusters_state[1].append(node)
                else:
                    self.__clusters_state[2].append(node)
            else:
                if 0 <= node.coordinates[1] <= self.__screen_height // 2:
                    self.__clusters_state[3].append(node)
                else:
                    self.__clusters_state[4].append(node)

    def get_cluster_id_by_node(self, node: BaseLeachNode) -> int:
        """Returns the cluster_id by the node"""
        if isinstance(node, BaseLeachStation):
            return 0

        for cluster_id, nodes in self.__clusters_state.items():
            if node in nodes:
                return cluster_id

    def get_nodes_by_cluster_index(self, cluster_index: int) -> list[BaseLeachNode]:
        return self.__clusters_state[cluster_index]
