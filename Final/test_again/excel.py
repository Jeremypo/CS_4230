import pandas as pd
import numpy as np  # Import numpy for handling infinity in a more standard way
import sys  # Import sys to handle command line arguments

def read_edge_list(file_path):
    edges = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:  # Check if line is not empty
                try:
                    node1, node2 = map(int, line.split())
                    edges.append((node1, node2))
                except ValueError:
                    print(f"Skipping invalid line {line_number}: '{line}' - line must contain exactly two integers")
    return edges

def create_adjacency_matrix(edges):
    max_node = max(max(pair) for pair in edges) + 1  # Find the largest node index
    matrix = [[float('inf')] * max_node for _ in range(max_node)]
    for node1, node2 in edges:
        matrix[node1][node2] = 1
        matrix[node2][node1] = 1  # Assuming undirected graph; remove if directed
    return matrix

def write_to_excel(matrix, output_file):
    df = pd.DataFrame(matrix)
    df.replace(np.inf, 'inf', inplace=True)
    df.to_excel(output_file, index=False, header=False)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]  # Get input file path from command line
    output_file = sys.argv[2]  # Get output file path from command line

    edges = read_edge_list(input_file)
    matrix = create_adjacency_matrix(edges)
    write_to_excel(matrix, output_file)
    print(f'Adjacency matrix written to {output_file}')

if __name__ == "__main__":
    main()
