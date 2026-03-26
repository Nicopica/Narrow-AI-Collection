from collections import defaultdict


class Graph:
    def __init__(self):
        self.edges = defaultdict(list)

    def add_connection(self, vertex_1, vertex_2, weight):
        self.edges[vertex_1].append((vertex_2, weight))
        self.edges[vertex_2].append((vertex_1, weight))

    def __str__(self):
        lines = []
        for node, neighbors in self.edges.items():
            neighbor_strings = [f"{neighbor} d:{weight}" for neighbor, weight in neighbors]
            formatted_neighbors = ", ".join(neighbor_strings)
            lines.append(f"{node} -> {formatted_neighbors}")
        return "\n".join(lines)
