import random

from network_protocols.buffers.messages import Message, Packet
from network_protocols.nodes.base import BaseFloodGateway, BaseFloodNode, BaseNodeProps, BaseLeachStation
from network_protocols.nodes.flood.node import FloodNode
from network_protocols.nodes.flood.gateway import FloodGateway
from network_protocols.nodes.funnel.node import FunnelNode
from network_protocols.nodes.funnel.station import FunnelStation
from network_protocols.nodes.leach.node import LeachNode
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


def leach_initializer(max_nodes_count: int, max_packets: int) -> list[BaseNodeProps]:
    nodes = [
        LeachNode(
            pos_x=random.randint(0, Config.SCREEN_WIDTH),
            pos_y=random.randint(0, Config.SCREEN_HEIGHT),
            radius=Config.NODE_RADIUS,
        ) for _ in range(max_nodes_count)
    ]

    nodes.append(
        LeachStation(
            pos_x=Config.SCREEN_WIDTH // 2,
            pos_y=Config.SCREEN_HEIGHT // 2,
            radius=Config.STATION_RADIUS,
        )
    )

    for node in nodes:
        node.find_neighbors(nodes=nodes)

    _initialize_packets(nodes=nodes, max_packets=max_packets)

    return nodes


def funnel_initializer(max_nodes_count: int, max_packets: int) -> list[BaseNodeProps]:
    nodes = [
        FunnelNode(
            pos_x=random.randint(0, Config.SCREEN_WIDTH),
            pos_y=random.randint(0, Config.SCREEN_HEIGHT),
            radius=Config.NODE_RADIUS,
        ) for _ in range(max_nodes_count)
    ]
    
    nodes.append(
        FunnelStation(
            pos_x=Config.SCREEN_WIDTH // 2,
            pos_y=Config.SCREEN_HEIGHT // 2,
            radius=Config.NODE_RADIUS,
        )
    )

    for node in nodes:
        node.find_neighbors(nodes=nodes)

    _initialize_packets(nodes=nodes, max_packets=max_packets)

    return nodes


def _initialize_packets(nodes: list[BaseFloodNode], max_packets: int) -> None:
    for node in nodes:
        if isinstance(node, BaseFloodGateway) or isinstance(node, BaseLeachStation):
            continue

        for _ in range(random.randint(0, max_packets)):
            node.buffer.put(
                Message(
                    data=Packet(owner_oid=node.oid),
                ),
            )
