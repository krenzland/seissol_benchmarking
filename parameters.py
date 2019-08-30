run_params_base = {
    'mesh_size': range(1,3),
    'order': [5, 6]
}

def process_run_config(config):
    config['mesh_file'] = 'snell_cube_{}'.format(config['mesh_size'])
    return config

def build_config_from_run(run_config):
    return {
        'order': run_config['order']
    }

job_params_base = {
    'time': '00:30:00',
    'project_id': 'pr45fi',
    'email': 'email@example.com',
    'nodes': 4,
    'ntasks_per_node': 1,
    'jobname': 'eaconv'
}

RUN_CONFIG = (run_params_base,
              process_run_config,
              build_config_from_run,
              ['run.sh', 'parameters.par'])
JOB_CONFIG = (job_params_base, 'job_supermuc_ng.job')

BUILD_CONFIG = ['build.sh']

TOOL_CONFIG = {
    'workdir_base': '/import/home/ga24dib/tmp/seissol_benchmarks/',
    'executable_name': 'SeisSol'
}

