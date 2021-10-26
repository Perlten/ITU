import fileinput
import sys
from typing import Container
import uuid
import random


class Edge:
    def __init__(self, capacity: int, source: 'Node', target: 'Node', is_reverse: bool = False) -> None:
        self.capacity_left = capacity
        self.capacity_used = 0

        self.source = source
        self.target = target

        self.reverse_edge = None
        self.is_reverse = is_reverse

        self.index_source = -1
        self.index_target = -1

    def can_flow_increase(self):
        return (self.capacity_left > 0 or self.capacity_left == -1)

    def change_flow(self, flow_bottleneck: int):
        self.capacity_used = self.capacity_used + flow_bottleneck
        if self.capacity_left != -1:
            self.capacity_left = self.capacity_left - flow_bottleneck

        reverse_edge = self.reverse_edge
        if reverse_edge.capacity_left != -1:
            reverse_edge.capacity_left = reverse_edge.capacity_left + flow_bottleneck


class Node:
    def __init__(self, name: str) -> None:
        self.outgoing_edges = []
        self.ingoing_edges = []
        self.name = name
        self.id = uuid.uuid4().hex


class Graph:
    def __init__(self, nodes: list = []) -> None:
        self.nodes = []
        self.nodes = nodes

    def __traceback(self, path_map: dict, source: Node, sink: Node) -> list:
        path = []
        current_edge = path_map[sink.id]
        while(current_edge.source.id != source.id):
            path.append(current_edge)
            current_edge = path_map.get(current_edge.source.id)

        path.append(current_edge)
        path.reverse()
        return path

    def bfs(self, source: Node, sink: Node, return_visited_on_empty=False):
        queue = [source]
        seen_nodes = {source}

        path_map = {}

        while(len(queue) != 0):
            current_node: Node = queue.pop(0)

            if(current_node == sink):
                return self.__traceback(path_map, source, sink)

            for edge in current_node.outgoing_edges:
                if(edge.target not in seen_nodes and edge.can_flow_increase()):
                    target_node = edge.target
                    path_map[target_node.id] = edge

                    queue.append(target_node)
                    seen_nodes.add(target_node)

        if (return_visited_on_empty):
            return list(seen_nodes)
        return []

    def solve(self, source: Node, sink: Node):
        pathway: list = self.bfs(source, sink)
        while(len(pathway) != 0):
            max_flow = [
                edge.capacity_left for edge in pathway if edge.capacity_left != -1]

            if(len(max_flow) == 0):
                print("infinite")
                return

            flow_bottleneck = min(max_flow)

            for edge in pathway:
                edge.change_flow(flow_bottleneck)

            pathway: list = self.bfs(source, sink)

        sink_flow = sum([edge.capacity_used for edge in sink.ingoing_edges])
        return sink_flow

    def min_cut(self, source: Node, sink: Node):
        nodes_in_cut: set = set(self.bfs(source, sink, True))

        min_cut = []
        for node in nodes_in_cut:
            for edge in node.outgoing_edges:
                target = edge.target
                if target not in nodes_in_cut:
                    min_cut.append(edge)

        return min_cut


def create_graph(node_names: list, edges: list, undirected=False) -> Graph:
    nodes = [Node(name) for name in node_names]

    for edge_data in edges:
        u, v, c = edge_data

        edge = Edge(c, nodes[u], nodes[v])
        edge.index_source = u
        edge.index_target = v

        reverse_edge = Edge(c if undirected else 0, nodes[v], nodes[u], True)

        edge.reverse_edge = reverse_edge
        reverse_edge.reverse_edge = edge

        reverse_edge.index_source = v
        reverse_edge.index_target = u

        nodes[u].outgoing_edges.append(edge)
        nodes[v].ingoing_edges.append(edge)

        nodes[u].ingoing_edges.append(reverse_edge)
        nodes[v].outgoing_edges.append(reverse_edge)

    G = Graph(nodes)
    return G


def main():
    node_names, edges = get_formatted_data()
    G = create_graph(node_names, edges, undirected=True)

    result = G.solve(G.nodes[0], G.nodes[-1])
    min_cut = G.min_cut(G.nodes[0], G.nodes[-1])
    check_res = sum([edge.capacity_used for edge in min_cut]) # For debugging

    print(result)
    print(check_res)
    for edge in min_cut:
        print(f"{edge.index_source} {edge.index_target} {edge.capacity_used}")

    return 0


def print_pathway(pathway: list):
    if(len(pathway) == 0):
        print("Could not find path")
        return

    for edge in pathway:
        print(edge.source.name + " - " + edge.target.name + " -- " +
              str(edge.capacity_used) + "/" + str(edge.capacity))

    print("--------------------------------------------")


def get_formatted_data():
    data_input = create_data_input()

    n = int(data_input.readline())

    nodes = [data_input.readline().strip() for _ in range(n)]
    m = int(data_input.readline())

    edges = [list(map(int, data_input.readline().strip().split(" ")))
             for _ in range(m)]

    return nodes, edges


def create_data_input() -> fileinput.FileInput:
    data = None
    if len(sys.argv) > 1:
        data = fileinput.input(sys.argv[1])
    else:
        data = fileinput.input()

    return data


if __name__ == "__main__":
    main()
