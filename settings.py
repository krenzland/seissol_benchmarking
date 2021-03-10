from abc import ABC, abstractmethod
from utils import product_dict, dict_subset_eq, dict_subset_idx_in_list
from copy import deepcopy

class RunConfigFactory:
    def __init__(self, base_params, process_run_config, make_build_config, run_files):
        self.base_params = base_params
        self.process_run_config = process_run_config
        self.make_build_config = make_build_config
        self.run_files = run_files
        self.run_configs_base = list(product_dict(**base_params))

    def make_configs(self, build_configs = None):
        if build_configs is None:
            build_configs = []
        run_configs = []
        run_id = 0
        build_config_id = len(build_configs)
        for run_id, run_config_base in enumerate(self.run_configs_base):
            run_config = self.process_run_config(run_config_base)
            build_config = self.make_build_config(run_config)

            #build_config_s = json.dumps(build_config)
            #if build_config_s not in build_configs_dict:
            #    build_configs_dict[build_config_s] = build_config_id
            #    build_config_id += 1

            run_config['run_id'] = run_id

            build_id = dict_subset_idx_in_list(build_config, build_configs)
            if build_id < 0:
                build_configs.append(build_config)
                build_id = build_config_id
                build_config_id += 1
            build_config['built'] = False
            build_config['build_id'] = build_id
            run_config['build_id'] = build_id

            run_configs.append(run_config)

        return run_configs, build_configs

class BuildConfigFactory:
    def __init__(self, build_files):
        self.build_files = build_files

class JobConfigFactory:
    def __init__(self, job_params_base, job_file, make_job_config):
        self.job_params_base = job_params_base
        self.job_file = job_file
        self.make_job_config = make_job_config

    def make_job_configs(self, run_configs, build_configs):
        # First create all possible job configs
        job_configs = []
        job_config_id = 0
        for run_config in run_configs:
            build_config = build_configs[run_config['build_id']]
            job_config = self.make_job_config(self.job_params_base, run_config, build_config)
            job_id = dict_subset_idx_in_list(job_config, job_configs)
            if job_id < 0:
                job_configs.append(job_config)
                job_id = job_config_id
                job_config_id += 1
            job_config['job_id'] = job_id
            run_config['job_id'] = job_id

        # Store list of runs for each job
        for run_config in run_configs:
            job_id = run_config['job_id']
            job_config = job_configs[job_id]
            if 'run_ids' not in job_config:
                job_config['run_ids'] = []
            job_config['run_ids'].append(run_config['run_id'])

        return job_configs

class Cluster(ABC):
    @abstractmethod
    def get_partition(self, number_of_nodes):
        pass

    @abstractmethod
    def get_cores_per_node(self):
        pass

    @abstractmethod
    def get_hyperthreading_factor(self):
        pass
