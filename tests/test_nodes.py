from network_protocols.utils.factories import _initialize_packets
from network_protocols.nodes.flood.node import FloodNode
from network_protocols.buffers.messages import Message, Packet


def test_coordinates():
    node = FloodNode(pos_x=10, pos_y=10)

    assert node.coordinates == (10, 10)


def test_non_neighbors():
    node = FloodNode(pos_x=10, pos_y=10)
    node.find_neighbors([])

    assert len(node.neighbors) == 0


def test_find_neighbors():
    node = FloodNode(pos_x=10, pos_y=10, radius=25)
    nodes = [
        FloodNode(pos_x=0, pos_y=10),
        FloodNode(pos_x=10, pos_y=0),
        FloodNode(pos_x=35, pos_y=20),
        FloodNode(pos_x=10, pos_y=-10),
    ]

    node.find_neighbors(nodes)

    assert len(node.neighbors) == 3


def test_clear_neighbors():
    node = FloodNode(pos_x=10, pos_y=10)
    neighbors = [
        FloodNode(pos_x=0, pos_y=10),
        FloodNode(pos_x=10, pos_y=0),
        FloodNode(pos_x=35, pos_y=20),
        FloodNode(pos_x=10, pos_y=-10),
    ]

    node.find_neighbors(neighbors)
    node.find_neighbors([])

    assert len(node.neighbors) == 0


def test_send_messages():
    nodes = [
        FloodNode(pos_x=10, pos_y=10),
        FloodNode(pos_x=0, pos_y=10),
        FloodNode(pos_x=10, pos_y=0),
        FloodNode(pos_x=35, pos_y=20),
        FloodNode(pos_x=10, pos_y=-10),
    ]

    _initialize_packets(nodes=nodes, max_packets=5)

    for node in nodes:
        node.send_messages(fpr=10)

        if len(node.neighbors):
            assert node.buffer.length == 0
            assert node.neighbors[0].buffer.length == 5


def test_send_messages_without_neighbors():
    node = FloodNode(pos_x=10, pos_y=10)

    node.buffer.put(
        data=Message(
            data=Packet(owner_oid=node.oid),
        )
    )

    node.send_messages(fpr=10)

    assert node.buffer.length == 0
