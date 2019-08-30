ulimit -Ss 2097152

export MP_SINGLE_THREAD=no
unset KMP_AFFINITY
export OMP_NUM_THREADS=94
export OMP_PLACES="cores(47)"

export XDMFWRITER_ALIGNMENT=8388608
export XDMFWRITER_BLOCK_SIZE=8388608
export SC_CHECKPOINT_ALIGNMENT=8388608

export SEISSOL_CHECKPOINT_ALIGNMENT=8388608
export SEISSOL_CHECKPOINT_DIRECT=1
export ASYNC_MODE=THREAD
export ASYNC_BUFFER_ALIGNMENT=8388608
source /etc/profile.d/modules.sh

module load slurm_setup
module load szip
module load libszip/2.1.1

cd {{ workdir }}
pwd
ls
mkdir output

mpiexec -n $SLURM_NTASKS ./SeisSol parameters.par
