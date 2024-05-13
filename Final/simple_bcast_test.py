from mpi4py import MPI

def simple_bcast():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        data = 100
    else:
        data = None
    data = comm.bcast(data, root=0)
    print("Rank", rank, "received", data)

if __name__ == "__main__":
    simple_bcast()
