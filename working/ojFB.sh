#!/bin/bash
#SBATCH --job-name=facebook_combined_OJ      # Job name
#SBATCH --nodes=8                  # Number of nodes (adjust as needed)
#SBATCH --ntasks=64                # Maximum number of tasks (processes)
#SBATCH --cpus-per-task=1          # Number of CPU cores per task
#SBATCH --output=output_%j.log     # Standard output and error log
#SBATCH --mail-type=END,FAIL       # Notifications for job done & fail
#SBATCH --mail-user=oj10102003@gmail.com  # Send-to email

# Load any modules you need
module load mpi

# Record the start time
echo "Job started at $(date)"

# Run the MPI program with different configurations
for ntasks in 4 8 16 32 64; do
    echo "Running with $ntasks tasks"
    start_time=$(date +%s)
    time mpiexec -np $ntasks python fwpFB.py
    end_time=$(date +%s)
    elapsed=$(( end_time - start_time ))
    echo "Elapsed time for $ntasks tasks: $elapsed seconds"
done

# Record the end time
echo "Job ended at $(date)"
