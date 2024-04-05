import networkx as nx
import matplotlib.pyplot as plt


def build_graph(file_path):
    directed_graph = nx.DiGraph()

    with open(file_path, 'r') as file:
        for line in file:
            node1, node2 = line.strip().split()
            directed_graph.add_edge(node1, node2)

    return directed_graph


def compute_centrality(graph):
    undirected_graph = graph.to_undirected()
    degree_cent = nx.degree_centrality(undirected_graph)
    closeness_cent = nx.closeness_centrality(undirected_graph)
    betweenness_cent = nx.betweenness_centrality(undirected_graph, normalized=True)

    return degree_cent, closeness_cent, betweenness_cent


def plot_histogram(data, title, xlabel, ylabel='Frequency'):
    plt.figure(figsize=(10, 6))
    plt.hist(data.values(), bins=50, alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == "__main__":
    #file_path = 'test.txt'
    file_path = 'twitter_combined.txt'
    graph = build_graph(file_path)
    degree, closeness, betweenness = compute_centrality(graph)

    plot_histogram(degree, 'Degree Centrality Histogram', 'Degree Centrality')
    plot_histogram(closeness, 'Closeness Centrality Histogram', 'Closeness Centrality')
    plot_histogram(betweenness, 'Betweenness Centrality Histogram', 'Betweenness Centrality')