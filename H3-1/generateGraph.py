import networkx as nx
import random
import time

start_time = time.time()


def generate_connected_graph(edges, seed=1):
    max_nodes_percentage = 4.5 / 100    # same ratio of nodes to edges in twitter
    max_nodes = max(int(edges * max_nodes_percentage), 2)
    G = nx.generators.trees.random_tree(n=max_nodes, seed=seed)
    while G.number_of_edges() < edges:
        a, b = random.sample(range(max_nodes), 2)
        if not G.has_edge(a, b):
            G.add_edge(a, b)
    return G


def write_edges_to_file(graph, file_path):
    with open(file_path, 'w') as file:
        for edge in graph.edges():
            file.write(f"{edge[0]} {edge[1]}\n")


x = 176814 # 10% of twitter number of nodes
graph = generate_connected_graph(x)

print(f"Number of edges: {graph.number_of_edges()}")
print(f"Number of nodes: {graph.number_of_nodes()}")

output_file = 'graph_edges.txt'
write_edges_to_file(graph, output_file)
end_time = time.time()
print(f"Edges written to {output_file}")
#print(f"Execution time: {end_time - start_time} seconds")
