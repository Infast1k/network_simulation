import pygame

from network_protocols.gui.base import BaseSimulation
from network_protocols.nodes.base import BaseFunnelStation, BaseNodeProps
from network_protocols.settings.config import Config
from network_protocols.utils.move import move_funnel_nodes


class FunnelSimulation(BaseSimulation):
    def __init__(self, nodes: list[BaseNodeProps]):
        super().__init__(nodes)
        self._station_color: tuple[int, int, int] = (255, 255, 0)

    def start(self) -> None:
        """Starts the network simulation"""
        pygame.init()

        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

                if event.type == pygame.KEYDOWN:
                    move_funnel_nodes(nodes=self._nodes)

            self._screen.fill("#1F1F1F")
            self._clock.tick(Config.FPS)

            self._draw_text_on_center(
                text="Press any key to move nodes...",
                screen_width=Config.SCREEN_WIDTH,
                y_pos=25,
            )
            self._draw_nodes()

            pygame.display.flip()

        pygame.quit()

    def _draw_nodes(self) -> None:
        """Draws the nodes and lines between neighbors"""
        for node in self._nodes:
            if isinstance(node, BaseFunnelStation):
                color = self._station_color
            else:
                color = self._node_color

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
