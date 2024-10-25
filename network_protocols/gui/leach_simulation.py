import pygame

from network_protocols.gui.base import BaseSimulation
from network_protocols.nodes.base import BaseLeachNode, BaseNodeProps, BaseLeachStation
from network_protocols.nodes.leach.manager import ClusterManager
from network_protocols.settings.config import Config
from network_protocols.utils.move import move_nodes


class LeachSimulation(BaseSimulation):
    def __init__(self, nodes: list[BaseNodeProps]):
        super().__init__(nodes)
        self._station_color: tuple[int, int, int] = (255, 255, 0)
        self._cluster_separetor_color: tuple[int, int, int] = (75, 112, 97)
        self._cluster_manager: ClusterManager = ClusterManager()

    def start(self) -> None:
        """Starts the network simulation"""
        pygame.init()

        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

                if event.type == pygame.KEYDOWN:
                    move_nodes(nodes=self._nodes, max_x=Config.SCREEN_WIDTH, max_y=Config.SCREEN_HEIGHT)
                    self._cluster_manager.initialize_clusters_state(nodes=self._nodes)
                    self._cluster_manager.find_cluster_heads()

                    for node in self._nodes:
                        if isinstance(node, BaseLeachStation):
                            node.find_neighbors(self._nodes)
                            node.receive_messages()
                            node.clear_buffer()
                        else:
                            cluster_id = self._cluster_manager.get_cluster_id_by_node(node)
                            cluster_neighbors = self._cluster_manager.get_nodes_by_cluster_index(cluster_id)

                            if node.is_cluster_head:
                                node.find_neighbors(nodes=cluster_neighbors)
                                node.receive_messages(nodes=cluster_neighbors, fpr=5)

            self._screen.fill("#1F1F1F")
            self._clock.tick(Config.FPS)
            self._separate_clusters()

            self._draw_text_on_center(
                text="Press any key to move nodes...",
                screen_width=Config.SCREEN_WIDTH,
                y_pos=25,
            )
            self._draw_nodes()

            pygame.display.flip()

        pygame.quit()

    def _separate_clusters(self) -> None:
        """Draw lines which separate clusters"""
        pygame.draw.line(
            surface=self._screen,
            color=self._cluster_separetor_color,
            start_pos=(Config.SCREEN_WIDTH // 2, 0),
            end_pos=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT),
            width=2,
        )

        pygame.draw.line(
            surface=self._screen,
            color=self._cluster_separetor_color,
            start_pos=(0, Config.SCREEN_HEIGHT // 2),
            end_pos=(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT // 2),
            width=2,
        )

    def _draw_nodes(self) -> None:
        """Draws the nodes and lines between neighbors"""
        for node in self._nodes:
            if isinstance(node, BaseLeachNode) and not node.is_cluster_head:
                color = self._node_color if node.buffer.length == 0 else self._node_with_pkgs_color
            elif isinstance(node, BaseLeachNode) and node.is_cluster_head:
                color = self._gateway_color
            elif isinstance(node, BaseLeachStation):
                color = self._station_color

            pygame.draw.circle(
                surface=self._screen,
                color=color,
                center=node.coordinates,
                radius=6,
            )

            for neighbor in node.neighbors:
                pygame.draw.line(
                    surface=self._screen,
                    color=self._line_color,
                    start_pos=node.coordinates,
                    end_pos=neighbor.coordinates,
                    width=2,
                )
