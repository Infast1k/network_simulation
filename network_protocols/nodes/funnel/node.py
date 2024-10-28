from network_protocols.nodes.base import BaseFunnelNode, BaseNodeProps


class FunnelNode(BaseFunnelNode):
    # TODO: rework this method
    def find_neighbors(self, nodes: list[BaseNodeProps]) -> None:
        return super().find_neighbors(nodes)
