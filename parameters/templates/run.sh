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

echo "run_id={{ run_id }}"

cd {{ workdir }}
pwd
ls
mkdir output

mpiexec -n $SLURM_NTASKS ./SeisSol parameters.par
