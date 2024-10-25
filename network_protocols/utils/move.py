from network_protocols.nodes.base import BaseLeachStation, BaseNodeProps
from network_protocols.nodes.leach.manager import ClusterManager
from network_protocols.settings.config import Config


def move_leach_nodes(nodes: list[BaseNodeProps], cluster_manager: ClusterManager) -> None:
    for node in nodes:
        if isinstance(node, BaseLeachStation):
            continue

        cluster_id = cluster_manager.get_cluster_id_by_node(node)

        if cluster_id == 1 or cluster_id == 3:
            min_y, max_y = 0, Config.SCREEN_HEIGHT // 2
        else:
            min_y, max_y = Config.SCREEN_HEIGHT // 2, Config.SCREEN_HEIGHT

        if cluster_id == 1 or cluster_id == 2:
            min_x, max_x = 0, Config.SCREEN_WIDTH // 2
        else:
            min_x, max_x = Config.SCREEN_WIDTH // 2, Config.SCREEN_WIDTH

        node.change_position(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
