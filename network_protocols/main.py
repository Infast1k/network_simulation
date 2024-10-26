import logging
import sys

from network_protocols.gui.funnel_simulation import FunnelSimulation
from network_protocols.gui.leach_simulation import LeachSimulation
from network_protocols.utils.factories import flood_initializer, funnel_initializer, leach_initializer
from network_protocols.gui.flood_simulation import FloodSimulation
from network_protocols.nodes.base import BaseNodeProps
from network_protocols.settings.config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def flood_algorithm() -> None:
    nodes: list[BaseNodeProps] = flood_initializer(
        max_nodes_count=Config.MAX_NODES,
        gateways_count=Config.MAX_GATEWAYS,
        max_packets=Config.MAX_PACKETS,
    )

    simulation = FloodSimulation(nodes=nodes)
    simulation.start()


def leach_algorithm() -> None:
    nodes: list[BaseNodeProps] = leach_initializer(
        max_nodes_count=Config.MAX_NODES,
        max_packets=Config.MAX_PACKETS,
    )

    simulation = LeachSimulation(nodes=nodes)
    simulation.start()


def funnel_algorithm() -> None:
    nodes: list[BaseNodeProps] = funnel_initializer(
        max_nodes_count=Config.MAX_NODES,
        max_packets=Config.MAX_PACKETS,
    )

    simulation = FunnelSimulation(nodes=nodes)
    simulation.start()


if __name__ == "__main__":
    try:
        match sys.argv[1]:
            case "flood":
                flood_algorithm()
            case "leach":
                leach_algorithm()
            case "funnel":
                funnel_algorithm()
            case _:
                raise IndexError
    except IndexError:
        logger.warning("Missing argument. Please provide the argument for specifying the simulation algorithm.")
