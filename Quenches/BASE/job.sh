#!/bin/bash
#SBATCH --ntasks=4               # total number of tasks across all nodes
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=4G       # memory per cpu-core (4G is default)
#SBATCH --time=144:00:00          # total run time limit (HH:MM:SS)
#SBATCH --job-name="Quench_PRESSURE_INDEX" 
#SBATCH --constraint=cascade

module purge
module load intel/2022.2.0
module load intel-mpi/intel/2021.7.0
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

############################################################################
# Run
############################################################################
EXE=/home/rm6309/software/lammps-stable_23Jun2022/build/lmp_della
srun $EXE -sf intel -in start.lmp
###########################################################################

date
