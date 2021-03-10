# TODO: Refactor this a bit and define a proper interface

from copy import deepcopy

def add_options_to_job_config(job_config_base, run_config, build_config, cluster):
    job_config = deepcopy(job_config_base)
    job_config['nodes'] = run_config['nodes']
    job_config['partition'] = cluster.get_partition(job_config['nodes'])
    job_config['ranks_per_node'] = run_config['ranks_per_node']
    job_config['build_id'] = run_config['build_id']
    rpn = job_config['ranks_per_node']
    if rpn == 1:
        job_config['cores_per_rank'] = cluster.get_cores_per_node() - 1
    elif rpn == 2:
        job_config['cores_per_rank'] = cluster.get_cores_per_node() // 2 - 1
    elif rpn == 4:
        job_config['cores_per_rank'] = cluster.get_cores_per_node() // 4 - 1

    job_config['threads_per_rank'] = cluster.get_hyperthreading_factor() * job_config['cores_per_rank']

    return job_config
