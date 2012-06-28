from datetime import datetime
from django.shortcuts import render
from django.conf import settings
import paramiko, base64, pickle, os
from MakerBarManager.presence.models import UserProfilePresence, Device
from paramiko.ssh_exception import AuthenticationException

def members_connected(request):

    rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
    router_address=settings.MAKERBAR_ROUTER_ADDRESS
    router_port = settings.MAKERBAR_ROUTER_PORT
    stdin, stdout, stderr =get_router_mac_addresses(rsa_key,router_address,router_port)

    attendance = set()
    for line in stdout:
        router_mac = line[10:27]
        try:
            e = UserProfilePresence.objects.get(device__mac=router_mac)
            attendance.add(e.user)
        except UserProfilePresence.DoesNotExist:
            pass
        except Device.DoesNotExist:
            pass

    output = ''
    for u in attendance:
        output += u.username + '\n'
        status_code=200 # Content
    if output == '':
        status_code = 204 # No content

    return render(request, 'members_connected.html', {'user_list':output},content_type="text/plain",status=status_code)

def who_is_connected(request):
    rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
    router_address=settings.MAKERBAR_ROUTER_ADDRESS
    router_port = settings.MAKERBAR_ROUTER_PORT
    stdin, stdout, stderr =get_router_mac_addresses(rsa_key,router_address,router_port)
    connected=set()
    for line in stdout:
        connected.add(line[10:27])

    output = ''
    for mac in connected:
        output += mac + '\n'
        status_code=200 # Content
    if output == '':
        status_code = 204 # No content
    return render(request, 'who_is_connected.html', {'connected_list':output},content_type="text/plain",status=status_code)

def get_router_mac_addresses(rsa_key,router_address,router_port):
    try:
        key = paramiko.RSAKey(data=base64.decodestring(rsa_key))
        client = paramiko.SSHClient()
        client.get_host_keys().add('[%s]:%d' % (router_address,router_port), 'ssh-rsa', key)
        wlauthkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser('~/MakerBarManager/keys/wlauth'))
        client.connect(router_address, username='root', port=router_port, pkey=wlauthkey)
        stdin, stdout, stderr = client.exec_command('wl assoclist')
        channel = stdout.channel
        status = channel.recv_exit_status()
        client.close()
    except AuthenticationException as e:
        stdin=''
        stdout=''
        stderr=''
        pass

    return stdin, stdout, stderr