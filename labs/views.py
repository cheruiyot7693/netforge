from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from academy.models import Lab
from .export import (
    build_containerlab_yaml,
    build_vrnetlab_json,
    build_openvpn_server_config,
    build_openvpn_client_config,
)

def lab_list(request):
    """Display list of available labs."""
    labs = Lab.objects.select_related('course').order_by('course__title', 'title')
    return render(request, 'labs/list.html', {'labs': labs})

def lab_detail(request, lab_id):
    """Display lab detail and SSH/VPN instructions."""
    lab = get_object_or_404(Lab, id=lab_id)
    vpn_lab = lab.topology_type == 'vpn'
    ssh_endpoints = []
    if vpn_lab:
        ssh_endpoints = [
            {
                'name': 'Core Switch',
                'host': '10.0.5.11',
                'user': 'admin',
                'description': 'SSH into the core switch over the VPN tunnel.',
            },
            {
                'name': 'Edge Router',
                'host': '10.0.5.12',
                'user': 'network',
                'description': 'SSH to the VPN edge router and verify BGP and IPsec.',
            },
            {
                'name': 'Linux Server',
                'host': '10.0.5.21',
                'user': 'ubuntu',
                'description': 'SSH into the lab server to run tests and validate connectivity.',
            },
        ]
    return render(request, 'labs/detail.html', {
        'lab': lab,
        'vpn_lab': vpn_lab,
        'ssh_endpoints': ssh_endpoints,
        'openvpn_server_config': build_openvpn_server_config(lab) if vpn_lab else None,
        'openvpn_client_config': build_openvpn_client_config(lab) if vpn_lab else None,
    })

def lab_start(request, lab_id):
    """Display lab start instructions."""
    lab = get_object_or_404(Lab, id=lab_id)
    vpn_lab = lab.topology_type == 'vpn'
    return render(request, 'labs/start.html', {
        'lab': lab,
        'vpn_lab': vpn_lab,
        'openvpn_server_config': build_openvpn_server_config(lab) if vpn_lab else None,
        'openvpn_client_config': build_openvpn_client_config(lab) if vpn_lab else None,
    })


def export_containerlab(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    yaml_content = build_containerlab_yaml(lab)
    return HttpResponse(yaml_content, content_type='application/x-yaml')


def export_vrnetlab(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    json_content = build_vrnetlab_json(lab)
    return HttpResponse(json_content, content_type='application/json')


def download_openvpn_server_config(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    if lab.topology_type != 'vpn':
        return HttpResponse('OpenVPN config is available only for VPN labs.', status=404)
    config = build_openvpn_server_config(lab)
    response = HttpResponse(config, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="lab-{lab_id}-openvpn-server.conf"'
    return response


def download_openvpn_client_config(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    if lab.topology_type != 'vpn':
        return HttpResponse('OpenVPN config is available only for VPN labs.', status=404)
    config = build_openvpn_client_config(lab)
    response = HttpResponse(config, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="lab-{lab_id}-openvpn-client.ovpn"'
    return response

def session_list(request):
    """Display list of lab sessions"""
    return render(request, 'labs/sessions.html')

def session_detail(request, session_id):
    """Display session detail"""
    return render(request, 'labs/session_detail.html', {'session_id': session_id})

def automation_list(request):
    """Display automation tasks"""
    return render(request, 'labs/automation.html')

def automation_detail(request, task_id):
    """Display automation task detail"""
    return render(request, 'labs/automation_detail.html', {'task_id': task_id})

def monitoring_dashboard(request):
    """Display NOC monitoring dashboard"""
    return render(request, 'labs/monitoring.html')
