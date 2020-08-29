import argparse
import os
import sys
import time

try:
    from ruamel.yaml import YAML
    from starlette.config import Config
except ModuleNotFoundError:
    os.system('python -m pip install --user ruamel.yaml starlette')
    sys.exit('Try again')


deploy_targets = ['worker', 'broker', 'backend']


def create_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    argparser.add_argument('command', choices=['up', 'down'], type=str, help='docker-compose action')
    argparser.add_argument('--target', choices=deploy_targets + ['all'], default='all',
                           type=str, help='service to start')
    return argparser


if __name__ == '__main__':
    args = create_argparser().parse_args()

    start_time = time.perf_counter()

    yaml = YAML()
    with open('deploy/config.yml', 'r', encoding='utf-8') as fp:
        config = yaml.load(fp)

    env_config = Config(config['context']['env_file'])
    env = env_config.get('ENV', default='dev')

    with open('deploy/docker-compose.yml', 'r', encoding='utf-8') as fp:
        compose = yaml.load(fp)

    if args.target != 'all':
        compose['services'] = {
            k: {kv: vv for kv, vv in v.items() if kv not in ['depends_on', 'links']}
            for k, v in compose['services'].items()
            if args.target in k
        }
    compose['services'] = {f'{k}-{env}': v for k, v in compose['services'].items()}
    if 'networks' in compose:
        compose['networks'] = {f'{k}-{env}': v for k, v in compose['networks'].items()}
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(f'deploy/docker-compose-{env}.yml', 'w', encoding='utf-8') as fp:
        yaml.dump(compose, fp)

    for task in config['tasks'][args.command]:
        print(f'\nTask "{task["title"]}": Started\n')
        try:
            for i, pipe in enumerate(task['pipeline']):
                command = pipe.format(ENV=env)
                print(f'Step {i + 1}: {command}\n')
                os.system(command)
        except Exception as e:
            print(f'\nTask "{task["title"]}": Skipping. {e}\n')
        finally:
            print(f'\nTask "{task["title"]}": Finished\n')

    print(f'\nDeploy has been finished. Processing time: {time.perf_counter() - start_time:.2f}s')
