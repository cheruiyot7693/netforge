import json
from typing import List

from academy.models import Lab


def serialize_lab(lab: Lab) -> dict:
    """Serialize a lab into a portable dictionary."""
    return {
        'id': lab.id,
        'title': lab.title,
        'description': lab.description,
        'course': {
            'id': lab.course.id,
            'title': lab.course.title,
            'level': lab.course.level,
        },
        'topology_type': lab.topology_type,
        'difficulty': lab.difficulty,
        'estimated_time': lab.estimated_time,
        'vpn_enabled': lab.topology_type == 'vpn',
        'nodes': build_lab_nodes(lab),
        'links': build_lab_links(lab),
    }


def build_lab_nodes(lab: Lab) -> List[dict]:
    if lab.topology_type == 'vpn':
        return [
            {'name': 'core-switch', 'type': 'switch', 'image': 'vrnetlab/nokia_srlinux:latest'},
            {'name': 'edge-router', 'type': 'router', 'image': 'vrnetlab/nokia_srlinux:latest'},
            {'name': 'linux-server', 'type': 'server', 'image': 'ubuntu:22.04'},
        ]
    return [
        {'name': 'router', 'type': 'router', 'image': 'vrnetlab/nokia_srlinux:latest'},
        {'name': 'linux-server', 'type': 'server', 'image': 'ubuntu:22.04'},
    ]


def build_lab_links(lab: Lab) -> List[dict]:
    if lab.topology_type == 'vpn':
        return [
            {'endpoints': ['core-switch:eth1', 'edge-router:eth1']},
            {'endpoints': ['edge-router:eth2', 'linux-server:eth1']},
        ]
    return [
        {'endpoints': ['router:eth1', 'linux-server:eth1']},
    ]


def build_containerlab_yaml(lab: Lab) -> str:
    nodes = build_lab_nodes(lab)
    links = build_lab_links(lab)
    lines = [f'name: netforge-lab-{lab.id}', 'topology:', '  nodes:']

    for node in nodes:
        lines.append(f'    {node["name"]}:')
        lines.append(f'      kind: linux')
        lines.append(f'      image: {node["image"]}')
        if node['type'] == 'server':
            lines.append('      mgmt_ipv4: 172.20.20.10/24')

    lines.append('  links:')
    for link in links:
        lines.append('    - endpoints: [' + ', '.join(link['endpoints']) + ']')

    return '\n'.join(lines) + '\n'


def build_vrnetlab_json(lab: Lab) -> str:
    payload = serialize_lab(lab)
    return json.dumps(payload, indent=2)


def build_openvpn_server_config(lab: Lab) -> str:
    topnet = '10.0.5.0 255.255.255.0' if lab.topology_type == 'vpn' else '10.0.10.0 255.255.255.0'
    return f"""port 1194
proto udp
dev tun
user nobody
group nogroup
persist-key
persist-tun
keepalive 10 120
cipher AES-256-CBC
auth SHA256
server 10.8.0.0 255.255.255.0
push \"route {topnet}\"
client-to-client
duplicate-cn
status /var/log/openvpn-status.log
log-append /var/log/openvpn.log
"""


def build_openvpn_client_config(lab: Lab, remote_host: str = 'vpn.example.com') -> str:
    return f"""client
dev tun
proto udp
remote {remote_host} 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
auth SHA256
verb 3
<ca>
# insert CA cert here
</ca>
<cert>
# insert client cert here
</cert>
<key>
# insert client key here
</key>
"""
