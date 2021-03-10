from settings import * 
run_params_base = {
    #'mesh_size': range(1,8),
    'mesh_size': range(1,4),
    #'order': [3,4,5,6],
    'order': [3,4],
    'material_file_base': ['/hppfs/work/pr45fi/ga24dib3/SeisSol/materials/material'],
    'scenario': ['snell'],
    'mesh_file_base': ['/hppfs/work/pr45fi/ga24dib3/SeisSol/meshes/convergence']
}

def process_run_config(config):
    config['mesh_file'] = '{}_{}/mesh_{}.h5'.format(config['mesh_file_base'],
                                                 config['scenario'],
                                                 config['mesh_size'])
    config['material_file'] = '{}_{}.yaml'.format(config['material_file_base'],
                                                  config['scenario'])
    return config

def build_config_from_run(run_config):
    return {
        'order': run_config['order']
    }

job_params_base = {
    'time': '00:30:00',
    'project_id': 'pr45fi',
    'email': 'lukas.krenz@in.tum.de',
    'nodes': 2,
    'ntasks_per_node': 1,
    'partition': 'micro',
    'job_name': 'ss_',
}

RUN_CONFIG = RunConfigFactory(
    base_params=run_params_base,
    process_run_config = process_run_config,
    make_build_config = build_config_from_run,
    run_files = ['run.sh', 'parameters.par', 'DGPATH']
)

def make_job_config(job_config_base, run_config, build_config):
    job_config = deepcopy(job_config_base)
    #job_config['run_id'] = run_config['run_id']
    job_config['build_id'] = run_config['build_id']
    node_cores = 48
    rank_cores = (node_cores // job_config['ntasks_per_node']) - 1 # commthread
    rank_threads = rank_cores * 2
    job_config['cores_per_rank'] = rank_cores
    job_config['threads_per_rank'] = rank_threads
    return job_config
              
JOB_CONFIG = JobConfigFactory(
    job_params_base=job_params_base,
    job_file='job_supermuc_ng.job',
    make_job_config=make_job_config)

BUILD_CONFIG = BuildConfigFactory(
    build_files = ['build.sh']
)

TOOL_CONFIG = {
    'workdir_base': './convergence_script/',
    'executable_name': 'SeisSol',
    'build_root': '/dss/dsshome1/0E/ga24dib3/src/SeisSol/'
}

