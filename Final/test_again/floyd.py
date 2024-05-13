from mpi4py import MPI
import pandas as pd
import numpy as np
import time
import sys  # Import sys to handle command line arguments

def read_matrix(file_path):
    df = pd.read_excel(file_path, header=None)
    matrix = df.values
    matrix[matrix == 'inf'] = np.inf
    return matrix

def floyd_warshall(matrix, rank, size):
    n = len(matrix)
    for k in range(n):
        # Broadcast the k-th row to all processes
        k_row = matrix[k, :] if rank == k % size else None
        k_row = comm.bcast(k_row, root=k % size)

        # Each process updates its rows of the matrix
        row_start = (n * rank) // size
        row_end = (n * (rank + 1)) // size
        for i in range(row_start, row_end):
            for j in range(n):
                matrix[i, j] = min(matrix[i, j], matrix[i, k] + k_row[j])

def write_matrix(matrix, file_path):
    df = pd.DataFrame(matrix)
    df.replace(np.inf, 'inf', inplace=True)
    df.to_excel(file_path, index=False, header=False)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Check for proper usage and argument passing
    if len(sys.argv) < 3:
        if rank == 0:
            print("Usage: mpiexec -n <num_processes> python script.py <input_file> <output_file>")
        sys.exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    start_time = time.time()

    if rank == 0:
        matrix = read_matrix(input_file)
    else:
        matrix = None

    # Broadcast the entire matrix to all processes
    matrix = comm.bcast(matrix, root=0)

    # Apply the Floyd-Warshall algorithm
    floyd_warshall(matrix, rank, size)

    # Gather the updated matrix at root
    result = comm.gather(matrix, root=0)

    # Reassemble the complete matrix at the root process
    if rank == 0:
        complete_matrix = np.vstack(result)
        write_matrix(complete_matrix, output_file)
        end_time = time.time()
        running_time = end_time - start_time
        print(f"Running time: {running_time} seconds")

        # Output the running time to a .txt file
        time_output_file = f"final{size}.txt"
        with open(time_output_file, "w") as f:
            f.write(f"Running time: {running_time} seconds\n")
