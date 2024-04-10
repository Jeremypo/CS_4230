import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import datetime


def build_graph(file_path):
    directed_graph = nx.DiGraph()

    with open(file_path, 'r') as file:
        for line in file:
            node1, node2 = line.strip().split()
            directed_graph.add_edge(node1, node2)

    undirected_graph = directed_graph.to_undirected()
    return undirected_graph


def compute_centrality_parallel(graph, centrality_func):
    return centrality_func(graph)


def compute_centrality(graph):
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(compute_centrality_parallel, [
            (graph, nx.degree_centrality),
            (graph, nx.closeness_centrality),
            (graph, nx.betweenness_centrality)
        ])
    return results


def plot_histogram(data, title, xlabel, ylabel='Frequency'):
    plt.figure(figsize=(10, 6))
    plt.hist(data.values(), bins=50, alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(title + '.png')
    plt.close()


def analyze_top_nodes(degree_cent, closeness_cent, betweenness_cent):
    top_nodes = sorted(degree_cent, key=degree_cent.get, reverse=True)[:200]
    closeness_values = [closeness_cent[node] for node in top_nodes]
    betweenness_values = [betweenness_cent[node] for node in top_nodes]

    closeness_stats = (np.mean(closeness_values), np.median(closeness_values), np.std(closeness_values))
    betweenness_stats = (np.mean(betweenness_values), np.median(betweenness_values), np.std(betweenness_values))

    return closeness_stats, betweenness_stats


if __name__ == "__main__":

    start_time = datetime.datetime.now()

    #file_path = 'twitter_combined.txt'
    #file_path = 'test.txt'
    file_path = 'graph_edges.txt'
    graph = build_graph(file_path)

    degree, closeness, betweenness = compute_centrality(graph)

    plot_histogram(degree, 'Degree_Centrality_Histogram', 'Degree Centrality')
    plot_histogram(closeness, 'Closeness_Centrality_Histogram', 'Closeness Centrality')
    plot_histogram(betweenness, 'Betweenness_Centrality_Histogram', 'Betweenness Centrality')

    closeness_stats, betweenness_stats = analyze_top_nodes(degree, closeness, betweenness)

    with open('centrality_analysis_results.txt', 'w') as file:
        file.write("Closeness (Mean, Median, Std): {}\n".format(closeness_stats))
        file.write("Betweenness (Mean, Median, Std): {}\n".format(betweenness_stats))

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    #print(f"Time: {execution_time} (Total)")
