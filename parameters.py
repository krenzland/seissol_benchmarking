run_params_base = {
    'mesh_size': range(1,3),
    'order': [5],
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
    'email': 'email@example.com',
    'nodes': 2,
    'ntasks_per_node': 1,
    'partition': 'micro',
    'job_name': 'eaconv'
}

RUN_CONFIG = (run_params_base,
              process_run_config,
              build_config_from_run,
              ['run.sh', 'parameters.par'])
JOB_CONFIG = (job_params_base, 'job_supermuc_ng.job')

BUILD_CONFIG = ['build.sh']

TOOL_CONFIG = {
    'workdir_base': '/import/home/ga24dib/tmp/seissol_benchmarks/',
    'executable_name': 'SeisSol',
    'build_root': '/dss/dsshome1/0E/ga24dib3/src/SeisSol/'
}

