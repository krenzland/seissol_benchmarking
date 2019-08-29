#!/usr/bin/env python3
import parameters

import os
import stat
import subprocess
from datetime import datetime
import itertools
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import json

def product_dict(**kwargs):
    # From https://stackoverflow.com/a/5228294
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))

def create_workdir(workdir_base):
    now = datetime.now()
    name = now.strftime('%Y-%b-%d_%H-%M_{counter}')
    counter = 0
    while True:
        cur_name = os.path.join(workdir_base, name.format(counter=counter))
        try:
            os.makedirs(cur_name)
            return cur_name
        except FileExistsError as err:
            counter += 1

def create_dirs_from_id(workdir_root,
                        prefix,
                        configs):
    id_name = "{}_id".format(prefix)
    for config in configs:
        print(config)
        workdir_name = "{}_{}".format(prefix,
                                          config[id_name])
        workdir_path = os.path.join(workdir_root, workdir_name)
        os.makedirs(workdir_path)
        config['workdir'] = workdir_path
            
def render_templates_from_dicts(template_env,
                                template_names,
                                tool_config,
                                configs,
                                executable=[False]):
    for template_name, ex in zip(template_names, executable):
        template = template_env.get_template(template_name)
        for config in configs:
            complete_config = {**tool_config, **config}
            file_name = os.path.join(config['workdir'], template_name)
            config['file_name'] = file_name
            print(file_name)
            with open(file_name, 'w') as f:
                f.write(template.render(complete_config, undefined=StrictUndefined))
            if ex:
                # chmod +x
                st = os.stat(file_name)
                os.chmod(file_name, st.st_mode | stat.S_IEXEC)

def build(build_configs):
    for build_config in build_configs:
        print(build_config['workdir'])
        result = subprocess.run(build_config['file_name'],
                                cwd=build_config['workdir'] + '/',
                                capture_output=True)
        for log_name, log in zip(['out', 'err'],
                                 [result.stdout, result.stderr]):
            file_name = '{}.log'.format(log_name)
            file_path = os.path.join(build_config['workdir'], file_name)
            with open(file_path, 'w') as f:
                if log:
                    f.write(log)


def symlink_build(run_configs, build_configs, tool_config):
    for run_config in run_configs:
        build_config = build_configs[run_config['build_id']]
        executable_dir = build_config['workdir']
        src_path = os.path.join(build_config['workdir'],
                                tool_config['executable_name'])
        dst_path = os.path.join(run_config['workdir'],
                                 tool_config['executable_name'])
        os.symlink(src=src_path, dst=dst_path)
        
def main():
    os.makedirs(parameters.TOOL_CONFIG['workdir_base'], exist_ok=True)
    workdir = create_workdir(workdir_base=parameters.TOOL_CONFIG['workdir_base'])
    print("Workdir = {}".format(workdir))

    template_env = Environment(loader=FileSystemLoader('templates'))
    
    run_config_bases = product_dict(**parameters.RUN_CONFIG[0])
    run_configs = []
    build_configs_dict = {}
    build_config_id = 0
    for run_id, run_config_base in enumerate(run_config_bases):
        run_config = parameters.RUN_CONFIG[1](run_config_base)
        build_config = json.dumps(parameters.RUN_CONFIG[2](run_config))
        if build_config not in build_configs_dict:
            build_configs_dict[build_config] = build_config_id
            build_config_id += 1

        run_config['build_id'] = build_configs_dict[build_config]
        run_config['run_id'] = run_id
        # TODO: Also append build config json to dict for debugging

        run_configs.append(run_config)

    build_configs = {}
    for k, v in build_configs_dict.items():
        build_config = json.loads(k)
        build_config['build_id'] = v
        build_configs[v] = build_config

    create_dirs_from_id(workdir, 'build', build_configs.values())
    create_dirs_from_id(workdir, 'run', run_configs)
    print(build_configs)
    print()

    print(run_configs)

    render_templates_from_dicts(template_env,
                                parameters.BUILD_CONFIG,
                                parameters.TOOL_CONFIG,
                                build_configs.values(),
                                executable=[True])
    #build(build_configs.values())
    #symlink_build(run_configs, build_configs, parameters.TOOL_CONFIG)

    render_templates_from_dicts(template_env,
                                parameters.RUN_CONFIG[3],
                                parameters.TOOL_CONFIG,
                                run_configs,
                                executable=[True, False])
    
        
    job_config = parameters.JOB_CONFIG[0]
    tool_config = parameters.TOOL_CONFIG

    template_name = parameters.JOB_CONFIG[1]
    config = job_config
    template = template_env.get_template(template_name)

    job_config['n_jobs'] = len(run_configs)
    job_config['run_configs'] = run_configs

    complete_config = {**tool_config, **job_config}
    file_name = os.path.join(workdir, template_name)
    config['file_name'] = file_name
    print(file_name)
    with open(file_name, 'w') as f:
        f.write(template.render(complete_config, undefined=StrictUndefined))

if __name__ == '__main__':
    main()
