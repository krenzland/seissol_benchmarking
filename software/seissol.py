# TODO: Refactor this a bit and define a proper interface

from copy import deepcopy

def add_options_to_job_config(job_config_base, run_config, build_config, cluster):
    job_config = deepcopy(job_config_base)
    job_config['nodes'] = run_config['nodes']
    job_config['partition'] = cluster.get_partition(job_config['nodes'])
    job_config['ranks_per_node'] = run_config['ranks_per_node']
    job_config['build_id'] = run_config['build_id']
    rpn = job_config['ranks_per_node']
    job_config['cores_per_rank'] = cluster.get_cores_per_node() // rpn - 1

    job_config['threads_per_rank'] = cluster.get_hyperthreading_factor() * job_config['cores_per_rank']

    # Hack: If cluster does not support array jobs, create a unique job config for each run
    if not cluster.is_slurm_array_supported():
      job_config['run_id'] = run_config['run_id']

    return job_config
