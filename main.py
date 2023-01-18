#!/usr/bin/env python3
from utils import product_dict, dict_subset_eq, dict_subset_idx_in_list, find_file_in_path

import importlib
import argparse
from collections import defaultdict
import sys
import os
import stat
import subprocess
from datetime import datetime
import itertools
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import json
import glob
from pathlib import Path

def create_workdir(workdir_base):
    now = datetime.now()
    name = now.strftime('%Y-%m-%d_%H-%M_{counter}')
    counter = 0
    while True:
        cur_name = os.path.join(workdir_base, name.format(counter=counter))
        try:
            os.makedirs(cur_name)
            return cur_name
        except FileExistsError as err:
            counter += 1

def create_unique_workdir_names(prefix, configs):
    name_counter = defaultdict(int) # Counts how often a name does occur
    id_key = "{}_id".format(prefix)
    workdir_key = "{}_name".format(prefix)
    # Ensure that all names are identical
    for config in configs:
        if workdir_key in config:
            name = config[workdir_key]
            name_counter[name] += 1
            # User has name preference, follow it
            counter = name_counter[name] - 1 # start by zero
            config[workdir_key] = "{}_{}_{}".format(prefix, config[workdir_key], counter)
        else:
            # No name -> use default name
            config[workdir_key] = "{}_{}".format(prefix, config[id_key])
    return configs

def create_dirs_from_id(workdir_root,
                        prefix,
                        configs):
    workdir_key = "{}_name".format(prefix)
    for config in configs:
        print(config)
        workdir_name = config[workdir_key]
        workdir_path = os.path.join(workdir_root, workdir_name)
        os.makedirs(workdir_path)
        config['workdir'] = workdir_path
            
def render_templates_from_dicts(template_env,
                                template_names,
                                tool_config,
                                search_paths,
                                configs,
                                executable=[False]):
    for template_name in template_names:
        template_base, _ = os.path.splitext(template_name)
        template = template_env.get_template(template_name)
        for config in configs:
            complete_config = {**tool_config, **config}
            file_name = os.path.join(config['workdir'], template_name)
            config['file_name_{}'.format(template_base)] = file_name
            if os.path.exists(file_name) and os.path.islink(file_name):
                os.remove(file_name)
            with open(file_name, 'w') as f:
                f.write(template.render(complete_config, undefined=StrictUndefined))
            if True: # TODO(Lukas) Reenable this feature!
                # chmod +x
                st = os.stat(file_name)
                os.chmod(file_name, st.st_mode | stat.S_IEXEC)

def build(build_configs):
    for build_config in build_configs:
        if 'built' in build_config and build_config['built']:
            print('Skipping build, reusing {}'.format(build_config['file_name_build']))
            continue
        file_name_build = build_config["file_name_build"]
        result = subprocess.run(file_name_build,
                                cwd=build_config['workdir'] + '/',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        for log_name, log in zip(['out', 'err'],
                                 [result.stdout, result.stderr]):
            file_name = 'build.{}'.format(log_name)
            file_path = os.path.join(build_config['workdir'], file_name)
            with open(file_path, 'wb') as f:
                if log:
                   f.write(log)
        if result.returncode != 0:
            raise Exception('Job {} failed!'.format(build_config['workdir']))
        build_config['built'] = True
        with open(os.path.join(build_config['workdir'], 'build.json'),
                  'w', encoding='utf-8') as f:
            json.dump(build_config, f, ensure_ascii=False, indent=4)


def symlink_build(run_configs, build_configs, tool_config):
    for run_config in run_configs:
        build_config = build_configs[run_config['build_id']]
        executable_dir = build_config['workdir']
        src_path = os.path.join(build_config['workdir'],
                                build_config['executable_name'])
        dst_path = os.path.join(run_config['workdir'],
                                 build_config['executable_name'])
        os.symlink(src=src_path, dst=dst_path)

def initialize_working_directory(run_configs, tool_config):
    for run_config in run_configs:
        wd = run_config['workdir']
        if 'run_root' in run_config:
            run_root = run_config['run_root']
        elif 'run_root' in tool_config:
            run_root = tool_config['run_root']
        else:
            continue

        files = glob.glob(run_root + "/*")
        for filename in files:
            basename = os.path.basename(filename)
            dst = os.path.join(wd, basename)
            os.symlink(src=filename, dst=dst)

def write_config_as_json(run_configs, build_configs, job_configs):
    for run_config in run_configs:
        job_id = run_config['job_id']
        job_config = job_configs[job_id]
        build_id = run_config['build_id']
        build_config = build_configs[build_id]
        path = run_config['workdir']

        configs = run_config, build_config, job_config
        filenames = "run", "build", "job"
        for filename, config in zip(filenames, configs):
            filename = os.path.join(run_config['workdir'],
                                    '{}.json'.format(filename))
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

def find_old_binaries():
    build_configs = []
    build_config_id = 0
    if args.reuse_binaries:
        files = glob.glob(args.reuse_binaries + '/**/build.json')
        max_build_config_id = 0
        for build_config_path in files:
            with open(build_config_path, 'r') as f:
                build_config = json.loads(f.read())
                build_configs.append(build_config)
                max_build_config_id = max(build_config_id, build_config['build_id'])
        build_config_id = max_build_config_id + 1

    return build_configs

def render_jobscripts(workdir, template_env, run_configs, job_configs):
    for job_config in job_configs:
        tool_config = parameters.TOOL_CONFIG
        template_name = parameters.JOB_CONFIG.job_file
        template = template_env.get_template(template_name)
        job_config['n_jobs'] = len(job_config['run_ids'])
        run_configs_job = []
        for run_id in job_config['run_ids']:
            run_config = run_configs[run_id]
            assert(run_config['run_id'] == run_id)
            run_configs_job.append(run_config)
            print(run_configs_job)
            job_config['run_configs'] = run_configs_job

        file_name = "{id}_{template}".format(id=job_config['job_id'],
                                            template=template_name)
        file_name = format(os.path.join(workdir, file_name))
        job_config['job_name'] += str(job_config['job_id'])
        job_config['file_name'] = file_name
        complete_config = {**tool_config, **job_config}
        complete_config['workdir'] = workdir
        print(complete_config)
        print(file_name)
        with open(file_name, 'w') as f:
            f.write(template.render(complete_config, undefined=StrictUndefined))
 
def main():
    # Also search for modules in working dir
    cwd = os.getcwd()
    sys.path.append(cwd)

    # Find path of current python script
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    
    parser = argparse.ArgumentParser(description='Create scripts from templates.')
    parser.add_argument('--reuse-binaries', help='Use binaries in workdir.')
    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Only print configurations')
    parser.add_argument("parameter_file", help="parameter file")
    args = parser.parse_args()

    # Load parameter settings from file
    global parameters
    parameters = importlib.import_module(args.parameter_file)

    if not args.dry_run:
        parameters.TOOL_CONFIG['workdir_base'] = \
            os.path.abspath(parameters.TOOL_CONFIG['workdir_base'])
        os.makedirs(parameters.TOOL_CONFIG['workdir_base'], exist_ok=True)
        workdir = create_workdir(workdir_base=parameters.TOOL_CONFIG['workdir_base'])
        print("Workdir = {}".format(workdir))

    template_search_path = ['./templates/', script_dir / "clusters"] + parameters.TOOL_CONFIG["search_paths"]
    template_env = Environment(loader=FileSystemLoader(template_search_path))
    
    run_configs, build_configs = parameters.RUN_CONFIG.make_configs(tool_config=parameters.TOOL_CONFIG)
    job_configs = parameters.JOB_CONFIG.make_job_configs(run_configs, build_configs)

    create_unique_workdir_names("build", build_configs)
    create_unique_workdir_names("run", run_configs)

    print(run_configs)
    print(build_configs)
    print(job_configs)
    if args.dry_run:
        return

    create_dirs_from_id(workdir, 'build', build_configs)
    create_dirs_from_id(workdir, 'run', run_configs)


    render_templates_from_dicts(template_env,
                                parameters.BUILD_CONFIG.build_files,
                                parameters.TOOL_CONFIG,
                                template_search_path,
                                build_configs,
                                executable=[True])
    build(build_configs)
    symlink_build(run_configs, build_configs, parameters.TOOL_CONFIG)

    initialize_working_directory(run_configs, parameters.TOOL_CONFIG)

    render_templates_from_dicts(template_env,
                                parameters.RUN_CONFIG.run_files,
                                parameters.TOOL_CONFIG,
                                template_search_path,
                                run_configs,
                                executable=[True, False, False])
    
    render_jobscripts(workdir,
                      template_env,
                      run_configs,
                      job_configs)

    # Make run config easy to analyze
    write_config_as_json(run_configs, build_configs, job_configs)
    
    # Create logdir
    os.makedirs(os.path.join(workdir, 'logs'))

if __name__ == '__main__':
    main()
