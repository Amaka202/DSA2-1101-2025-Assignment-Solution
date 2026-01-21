# TASK 2: Minimum Spanning Tree.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx


# =========================
# Union-Find (Disjoint Set)
# =========================

@dataclass
class UnionFind:
    parent: Dict[Hashable, Hashable]
    rank: Dict[Hashable, int]

    @classmethod
    def from_nodes(cls, nodes: List[Hashable]) -> "UnionFind":
        return cls(
            parent={n: n for n in nodes},
            rank={n: 0 for n in nodes},
        )

    def find(self, x: Hashable) -> Hashable:
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: Hashable, b: Hashable) -> bool:
        # Returns True if merged, False if already connected (cycle)
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False

        # Union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

        return True


# ==========================================
# REQUIRED FUNCTION: MyMinimumSpanningTree
# ==========================================

def MyMinimumSpanningTree(Graph: nx.Graph) -> nx.Graph:
    """
    Minimum Spanning Tree using Kruskal's algorithm.

    Signature required by the assignment:
        def MyMinimumSpanningTree(Graph) -> Graph

    Input:  connected, undirected, weighted NetworkX graph
    Output: MST as a NetworkX graph
    """
    if Graph is None:
        raise ValueError("Graph is None.")
    if Graph.is_directed():
        raise ValueError("Graph must be undirected.")
    if Graph.number_of_nodes() == 0:
        return nx.Graph()
    if not nx.is_connected(Graph):
        raise ValueError("Graph must be connected.")
    for _, _, data in Graph.edges(data=True):
        if "weight" not in data:
            raise ValueError("Every edge must have a 'weight' attribute.")

    # Collect and sort edges by weight
    edges: List[Tuple[Hashable, Hashable, float]] = []
    for u, v, data in Graph.edges(data=True):
        edges.append((u, v, float(data["weight"])))
    edges.sort(key=lambda e: e[2])

    mst = nx.Graph()
    mst.add_nodes_from(Graph.nodes())

    uf = UnionFind.from_nodes(list(Graph.nodes()))

    # Step-by-step console output
    name = Graph.graph.get("name", "Graph")
    print("\n==============================")
    print(f"Building MST for: {name}")
    print("Algorithm: Kruskal")
    print(f"Nodes: {Graph.number_of_nodes()} | Edges: {Graph.number_of_edges()}")
    print("==============================")

    print("\nEdges sorted by weight (u, v, w):")
    for u, v, w in edges:
        print(f"  ({u}, {v}, {w})")

    print("\nStep-by-step selection:")
    total_weight = 0.0

    for u, v, w in edges:
        if uf.union(u, v):
            mst.add_edge(u, v, weight=w)
            total_weight += w
            print(f"  ADD  ({u}, {v}) w={w} | mst_edges={mst.number_of_edges()} | total={total_weight}")
        else:
            print(f"  SKIP ({u}, {v}) w={w} | would create a cycle")

        if mst.number_of_edges() == Graph.number_of_nodes() - 1:
            break

    print(f"\nDone. MST total weight = {total_weight}")
    return mst


# =========================
# Drawing helper
# =========================

def draw_weighted_graph(G: nx.Graph, title: str, filename: str) -> None:
    """
    Draw the graph and save it as an image file.
    """
    plt.figure()
    pos = nx.spring_layout(G, seed=42)  # stable layout for repeatable screenshots
    nx.draw_networkx(G, pos=pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close()


# =========================
# Build the 3 required graphs
# =========================

def build_graph_1() -> nx.Graph:
    """
    Graph 1: connected graph with 6 nodes and 10 edges.
    """
    G = nx.Graph()
    G.graph["name"] = "Graph 1 (6 nodes, 10 edges)"
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_weighted_edges_from([
        (0, 1, 4),
        (0, 2, 2),
        (0, 3, 7),
        (1, 2, 1),
        (1, 4, 3),
        (2, 3, 5),
        (2, 4, 8),
        (2, 5, 10),
        (3, 5, 6),
        (4, 5, 9),
    ])
    return G


def build_graph_2() -> nx.Graph:
    """
    Graph 2: connected graph with at least 5 nodes and at least 8 edges.
    """
    G = nx.Graph()
    G.graph["name"] = "Graph 2 (6 nodes, 9 edges)"
    G.add_nodes_from(["A", "B", "C", "D", "E", "F"])
    G.add_weighted_edges_from([
        ("A", "B", 3),
        ("A", "C", 1),
        ("A", "D", 4),
        ("B", "C", 2),
        ("B", "E", 6),
        ("C", "D", 5),
        ("C", "E", 7),
        ("D", "F", 8),
        ("E", "F", 9),
    ])
    return G


def build_graph_3() -> nx.Graph:
    """
    Graph 3: connected graph with at least 5 nodes and at least 8 edges.
    """
    G = nx.Graph()
    G.graph["name"] = "Graph 3 (7 nodes, 11 edges)"
    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
    G.add_weighted_edges_from([
        (1, 2, 9),
        (1, 3, 3),
        (1, 4, 6),
        (2, 3, 5),
        (2, 5, 7),
        (3, 4, 2),
        (3, 6, 4),
        (4, 6, 8),
        (5, 6, 1),
        (5, 7, 10),
        (6, 7, 11),
    ])
    return G


# =========================
# Run and generate outputs
# =========================

def main() -> None:
    graphs = [build_graph_1(), build_graph_2(), build_graph_3()]

    for idx, G in enumerate(graphs, start=1):
        draw_weighted_graph(
            G,
            title=f"Original {G.graph.get('name', f'Graph {idx}')}",
            filename=f"graph{idx}_original.png",
        )

        mst = MyMinimumSpanningTree(G)

        draw_weighted_graph(
            mst,
            title=f"MST of {G.graph.get('name', f'Graph {idx}')}",
            filename=f"graph{idx}_mst.png",
        )

    print("\nSaved image files:")
    print("  graph1_original.png, graph1_mst.png")
    print("  graph2_original.png, graph2_mst.png")
    print("  graph3_original.png, graph3_mst.png")


if __name__ == "__main__":
    main()
