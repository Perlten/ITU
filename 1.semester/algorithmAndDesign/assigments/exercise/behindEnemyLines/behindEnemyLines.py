import fileinput
import sys
from typing import Container
import uuid
import random


class Edge:
    def __init__(self, capacity: int, source: 'Node', target: 'Node') -> None:
        self.capacity_left = capacity
        self.capacity_used = 0

        self.source = source
        self.target = target

        self.reverse_edge = None

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

    def bfs(self, source: Node, sink: Node, returnEmptyList=True):

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
        if (returnEmptyList):
            return []
        return path_map

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
        # path = list(self.bfs(source, sink, returnEmptyList=False).values())
        seen_nodes: set = set()
        node_queue = [source]

        while(len(node_queue) != 0):
            current_node = node_queue.pop(0)
            outgoing_nodes = [edge.target for edge in current_node.outgoing_edges if edge.capacity_left > 0 and edge.target not in seen_nodes]

            print(outgoing_nodes)


    def brute_force_min_cut(self, source: Node, sink: Node):
        cut: set = {source}

        min_cut_value = sys.maxsize
        min_cut = {}

        for outer_node in self.nodes[1: - 1]:
            for inner_node in self.nodes[1: -1]:
                temp_cut = cut.copy()
                temp_cut.add(inner_node)

                temp_min_cut_value = 0

                for current_node in temp_cut:
                    for edge in current_node.outgoing_edges:
                        target_node = edge.target
                        if target_node not in temp_cut:
                            if edge.capacity_left < 0:
                                temp_min_cut_value = sys.maxsize
                            else:
                                temp_min_cut_value = temp_min_cut_value + edge.capacity_left

                if temp_min_cut_value != 0 and min_cut_value > temp_min_cut_value:
                    min_cut_value = temp_min_cut_value
                    min_cut = temp_cut.copy()

                temp_cut.add(outer_node)

            cut.add(outer_node)

        return min_cut_value, min_cut


def create_graph(node_names: list, edges: list, undirected=False) -> Graph:
    nodes = [Node(name) for name in node_names]

    for edge_data in edges:
        u, v, c = edge_data
        edge = Edge(c, nodes[u], nodes[v])

        reverse_edge = Edge(c if undirected else 0, nodes[v], nodes[u])

        edge.reverse_edge = reverse_edge
        reverse_edge.reverse_edge = edge

        nodes[u].outgoing_edges.append(edge)
        nodes[v].ingoing_edges.append(edge)

        nodes[u].ingoing_edges.append(reverse_edge)
        nodes[v].outgoing_edges.append(reverse_edge)

    G = Graph(nodes)
    return G


def main():
    node_names, edges = get_formatted_data()
    G = create_graph(node_names, edges, undirected=False)

    brute_force_min_cut_value, min_cut = G.brute_force_min_cut(G.nodes[0], G.nodes[-1])

    result = G.solve(G.nodes[0], G.nodes[-1])
    min_cut = G.min_cut(G.nodes[0], G.nodes[-1])

    if brute_force_min_cut_value == result:
        print(f"It works: {result}")
    else:
        print(f"It does not work. Result: {result} should be: {min_cut}")


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
