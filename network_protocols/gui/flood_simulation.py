import pygame

from network_protocols.gui.base import BaseSimulation
from network_protocols.nodes.base import BaseFloodNode
from network_protocols.settings.config import Config
from network_protocols.utils.move import move_flood_nodes


class FloodSimulation(BaseSimulation):
    def start(self) -> None:
        """Starts the network simulation"""
        pygame.init()

        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

                if event.type == pygame.KEYDOWN:
                    move_flood_nodes(nodes=self._nodes)

                    for node in self._nodes:
                        node.find_neighbors(self._nodes)

                        if isinstance(node, BaseFloodNode):
                            node.send_messages(fpr=Config.FPR)
                        else:
                            node.clear_buffer()

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
