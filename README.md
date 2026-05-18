# NetForge Academy

NetForge Academy is a Django-based ISP training platform built for network engineering labs, course browsing, and infrastructure automation.

## What it includes

- `academy` app for dashboard and course/lab metadata
- `courses` app for browsing courses and enrolling
- `labs` app for lab browsing, lab details, and VPN-enabled lab access
- `users` app for authentication and profile management
- `payments` app stub for payment/checkout flows

## Labs workflow

This project is designed for lab exercises where users can:

1. Browse available labs under `/labs/`
2. Open a lab detail page for lab-specific configuration
3. Build VPN topology and get OpenVPN configuration
4. Connect to routers, switches, and lab servers over VPN
5. Download Containerlab and VRNetLab definitions for infrastructure deployment

## VPN and SSH access

VPN labs are identified by `topology_type == 'vpn'`.

On a VPN lab page, users can:

- View generated OpenVPN server and client config
- Download `server.conf` and `client.ovpn`
- Use SSH commands for routers and servers inside the lab

Example SSH commands:

```bash
ssh admin@10.0.5.11
ssh network@10.0.5.12
ssh ubuntu@10.0.5.21
```

## Export options

For each lab, users can export:

- Containerlab topology YAML
- VRNetLab JSON definition

These exports simplify container-based infrastructure deployment and lab automation.

## Running locally

1. Create a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

5. Open `http://localhost:8000/`

## Notes

- The app is currently configured for development with `DEBUG=True`.
- OpenVPN config is synthesized from lab topology metadata.
- The repository includes sample courses and labs.

## Next steps

- Add real Containerlab/VRNetLab deploy scripts
- Add lab session state tracking and provisioning
- Add VPN certificate/key generation and secure OpenVPN server deployment
- Create a separate lab infrastructure project under `lab_infra/` for Containerlab and VRNetLab deployment
- Use `lab_infra/run_lab.py` to deploy Containerlab topologies and validate VRNetLab definitions
