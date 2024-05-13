from mpi4py import MPI
import numpy as np
import sys
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def floyd_warshall(part_matrix, n, p_rows):
    for k in range(n):
        row_k = np.zeros(n, dtype=int) if rank != k // p_rows else part_matrix[k % p_rows].copy()
        comm.Bcast(row_k, root=k // p_rows)
        for i in range(p_rows):
            for j in range(n):
                part_matrix[i, j] = min(part_matrix[i, j], part_matrix[i, k] + row_k[j])

def read_graph_from_file(filename):
    if rank == 0:
        print("Beginning to read the edges from the file...")
    with open(filename, 'r') as file:
        graph = [list(map(int, line.split())) for line in file.readlines()]
    if rank == 0:
        print("Finished reading the edges from the file.")
    return np.array(graph)

def calculate_centrality(part_matrix, n, p_rows):
    closeness = np.zeros(p_rows)
    for i in range(p_rows):
        closeness[i] = (n - 1) / np.sum(part_matrix[i]) if np.sum(part_matrix[i]) > 0 else 0
        # Print message for each node's centrality calculation
        if rank == 0:
            print(f"Centrality for node {i} calculated by process {rank}: {closeness[i]}")
    return closeness

# Main execution block
if len(sys.argv) != 2:
    if rank == 0:
        print("Usage: mpiexec -n <num_procs> python script.py <path_to_graph_file>")
    sys.exit()

filename = sys.argv[1]

# Initialize the graph and distribute it
if rank == 0:
    print("Starting to build the graph...")
    complete_graph = read_graph_from_file(filename)
    n = complete_graph.shape[0]
    # Distribute parts of the matrix to each process
    for i in range(1, size):
        p_rows = n // size + (1 if i < n % size else 0)
        start_row = sum(n // size + (1 if x < n % size else 0) for x in range(i))
        end_row = start_row + p_rows
        comm.Send(complete_graph[start_row:end_row, :], dest=i)
    local_rows = complete_graph[:n // size + (1 if 0 < n % size else 0), :]
    print("Finished building the graph.")
else:
    n = None

# Broadcast n to all processors
n = comm.bcast(n, root=0)
p_rows = n // size + (1 if rank < n % size else 0)
local_rows = np.zeros((p_rows, n), dtype=int) if rank != 0 else local_rows

if rank != 0:
    comm.Recv(local_rows, source=0)

# Measure the runtime of the computation
start_time = MPI.Wtime()

# Run the Floyd-Warshall algorithm
floyd_warshall(local_rows, n, p_rows)

# Calculate local centrality
local_centrality = calculate_centrality(local_rows, n, p_rows)

# Gather all centralities at root
all_centrality = None
if rank == 0:
    all_centrality = np.zeros(n)
comm.Gather(local_centrality, all_centrality, root=0)

end_time = MPI.Wtime()

# Output results and runtime
if rank == 0:
    #print("Closeness centrality:", all_centrality)
    print("Total runtime: {:.2f} seconds".format(end_time - start_time))
    # Further processing for output.txt and screen display can be added here
