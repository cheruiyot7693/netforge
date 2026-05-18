# Lab Infrastructure Project

This separate project contains scripts for deploying lab topologies using Containerlab and validating VRNetLab definitions.

## Purpose

The `lab_infra` project is a standalone helper for building and running network lab infrastructure.
It is separate from the main Django application and focuses on container-based lab orchestration.

## Features

- Run a Containerlab topology from a YAML file
- Destroy a Containerlab topology
- Validate a VRNetLab JSON definition
- Generate OpenVPN config files in the main repo through Django lab exports

## Usage

### Deploy Containerlab

```bash
python lab_infra/run_lab.py --deploy-containerlab path/to/topology.yml
```

### Destroy Containerlab

```bash
python lab_infra/run_lab.py --destroy-containerlab path/to/topology.yml
```

### Validate VRNetLab JSON

```bash
python lab_infra/run_lab.py --validate-vrnetlab path/to/lab.json
```

### Deploy VRNetLab

This script does not automatically deploy VRNetLab. It validates the JSON definition and provides a project entry point.

```bash
python lab_infra/run_lab.py --deploy-vrnetlab path/to/lab.json
```

## Requirements

- Python 3.11+
- `containerlab` CLI installed for containerlab deploy/destroy commands

## Notes

- The main Django app can export lab definitions to Containerlab YAML and VRNetLab JSON.
- Use those exported files with this runner to deploy the infrastructure.
- OpenVPN configuration is generated inside the main repo’s lab pages, then used to connect into the lab environment.
