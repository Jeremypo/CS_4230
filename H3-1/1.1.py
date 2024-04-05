import networkx as nx
import matplotlib.pyplot as plt

def convert_generate(file_path):
    directed_graph = nx.read_edgelist(file_path, create_using=nx.DiGraph())
    undirected_graph = directed_graph.to_undirected()

    degree_cent = nx.degree_centrality(undirected_graph)
    closeness_cent = nx.closeness_centrality(undirected_graph)
    betweenness_cent = nx.betweenness_centrality(undirected_graph)

    return degree_cent, closeness_cent, betweenness_cent


def plot_histogram(data, title, xlabel, ylabel='Frequency'):
    plt.figure(figsize=(10, 6))
    plt.hist(data.values(), bins=20, alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == "__main__":
    #file_path = 'C:/GitHub/CS_4230/H3-1/test.txt'
    file_path = 'C:/GitHub/CS_4230/H3-1/twitter_combined.txt'
    degree, closeness, betweenness = convert_generate(file_path)

    plot_histogram(degree, 'Degree Centrality Histogram', 'Degree Centrality')
    plot_histogram(closeness, 'Closeness Centrality Histogram', 'Closeness Centrality')
    plot_histogram(betweenness, 'Betweenness Centrality Histogram', 'Betweenness Centrality')