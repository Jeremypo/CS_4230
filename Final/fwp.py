from mpi4py import MPI
import numpy as np
import time


def floyd_warshall_parallel(num_nodes, edges):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    inf = float('inf')
    dist = np.full((num_nodes, num_nodes), inf)

    for i in range(num_nodes):
        dist[i, i] = 0

    for u, v in edges:
        dist[u, v] = 1
        dist[v, u] = 1

    start_time = time.time()
    for k in range(num_nodes):
        row_k = dist[k, :].copy()  # Make a copy of the row to ensure a contiguous buffer
        comm.Bcast(row_k, root=0)

        rows_per_proc = (num_nodes + size - 1) // size
        i_start = rows_per_proc * rank
        i_end = min(i_start + rows_per_proc, num_nodes)

        for i in range(i_start, i_end):
            for j in range(num_nodes):
                dist[i, j] = min(dist[i, j], dist[i, k] + row_k[j])

    # Gathering results
    if rank == 0:
        full_dist = np.empty_like(dist)
        comm.Gather(dist[i_start:i_end, :], full_dist, root=0)
    else:
        comm.Gather(dist[i_start:i_end, :], None, root=0)

    end_time = time.time()

    if rank == 0:
        return end_time - start_time, full_dist
    else:
        return None


edges = []
filename = "test.txt"
with open(filename, 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) == 2:
            try:
                u, v = map(int, parts)
                edges.append((u, v))
            except ValueError:
                continue

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank == 0:
    max_node = max(max(u, v) for u, v in edges) + 1
    run_time, _ = floyd_warshall_parallel(max_node, edges)
    if _ is not None:
        print("Time taken: {:.3f} seconds".format(run_time))
