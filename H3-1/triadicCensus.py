import networkx as nx

twitter_graph = nx.read_edgelist('graph_edges.txt', create_using=nx.DiGraph)

triadic_census = nx.algorithms.triads.triadic_census(twitter_graph)

with open('triadic_census_results.txt', 'w') as file:
    for triad_type, count in triadic_census.items():
        file.write(f"{triad_type}: {count}\n")

print("Triadic census results have been written to triadic_census_results.txt")
