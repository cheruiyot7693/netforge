#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def run_command(command, cwd=None, capture_output=False):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=False,
    )
    if capture_output:
        return result
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}\nExit {result.returncode}")
    return result


def deploy_containerlab(topology_file: Path):
    if not shutil.which('containerlab'):
        raise RuntimeError('containerlab is not installed or not on PATH')

    topology_file = topology_file.resolve()
    run_command(['containerlab', 'deploy', '-t', str(topology_file)])
    print('Containerlab deployment started')


def destroy_containerlab(topology_file: Path):
    if not shutil.which('containerlab'):
        raise RuntimeError('containerlab is not installed or not on PATH')

    topology_file = topology_file.resolve()
    run_command(['containerlab', 'destroy', '-t', str(topology_file)])
    print('Containerlab topology destroyed')


def validate_vrnetlab(json_file: Path):
    json_file = json_file.resolve()
    with json_file.open() as fh:
        payload = json.load(fh)
    required = ['title', 'description', 'topology_type', 'difficulty', 'estimated_time', 'course']
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f'Missing VRNetLab fields: {missing}')
    print(f'VRNetLab JSON for {payload.get("title")} is valid')


def deploy_vrnetlab(json_file: Path):
    validate_vrnetlab(json_file)
    print('VRNetLab deployment is not yet automated in this script.')
    print('Use VRNetLab tooling separately with the generated JSON definition.')


def main():
    parser = argparse.ArgumentParser(description='Lab infrastructure runner for containerlab and VRNetLab')
    parser.add_argument('--deploy-containerlab', type=Path, help='Path to a containerlab topology YAML file')
    parser.add_argument('--destroy-containerlab', type=Path, help='Path to a containerlab topology YAML file to destroy')
    parser.add_argument('--validate-vrnetlab', type=Path, help='Validate a VRNetLab JSON definition')
    parser.add_argument('--deploy-vrnetlab', type=Path, help='Validate and prepare VRNetLab JSON definition')

    args = parser.parse_args()

    if args.deploy_containerlab:
        deploy_containerlab(args.deploy_containerlab)
    elif args.destroy_containerlab:
        destroy_containerlab(args.destroy_containerlab)
    elif args.validate_vrnetlab:
        validate_vrnetlab(args.validate_vrnetlab)
    elif args.deploy_vrnetlab:
        deploy_vrnetlab(args.deploy_vrnetlab)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
