import random
from network_protocols.buffers.messages import Message, Packet
from network_protocols.nodes.base import BaseGateway, BaseNode, BaseNodeProps, BaseStation
from network_protocols.nodes.flood.node import FloodNode
from network_protocols.nodes.flood.gateway import FloodGateway
from network_protocols.nodes.leach.station import LeachStation
from network_protocols.settings.config import Config


def flood_initializer(max_nodes_count: int, gateways_count: int, max_packets: int) -> list[BaseNodeProps]:
    nodes = [
        FloodNode(
            pos_x=random.randint(0, Config.SCREEN_WIDTH),
            pos_y=random.randint(0, Config.SCREEN_HEIGHT),
            radius=100,
        ) for _ in range(max_nodes_count)
    ]

    nodes.extend(
        FloodGateway(
            pos_x=random.randint(0, Config.SCREEN_WIDTH),
            pos_y=random.randint(0, Config.SCREEN_HEIGHT),
        ) for _ in range(gateways_count)
    )

    for node in nodes:
        node.find_neighbors(nodes)

    _initialize_packets(nodes=nodes, max_packets=max_packets)

    return nodes


def leach_initializer(max_nodes_count: int, gateways_count: int, max_packets: int) -> list[BaseNodeProps]:
    nodes = [LeachStation(
        pos_x=Config.SCREEN_WIDTH // 2,
        pos_y=Config.SCREEN_HEIGHT // 2,
        radius=Config.STATION_RADIUS,
    )]

    return nodes


def _initialize_packets(nodes: list[BaseNode], max_packets: int) -> None:
    for node in nodes:
        if isinstance(node, BaseGateway) or isinstance(node, BaseStation):
            continue

        for _ in range(random.randint(0, max_packets)):
            node.buffer.put(
                Message(
                    data=Packet(owner_oid=node.oid),
                ),
            )
