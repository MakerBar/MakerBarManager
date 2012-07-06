<<<<<<< HEAD
from django.shortcuts import render
from django.conf import settings
import paramiko, base64, pickle, os, datetime
from datetime import datetime, timedelta
from MakerBarManager.presence.models import UserProfilePresence, Device, UsageLog
from paramiko.ssh_exception import AuthenticationException

def members_connected(request,lookback=0):
    int_lookback=int(lookback)
    if int_lookback>0 or int_lookback<=1440*2:
        #Check the presence logs back lookback number of minutes for activity
        s_dte=datetime.today()
        e_dte=s_dte+timedelta(minutes=-int_lookback)
        logs = UsageLog.objects.filter(use_date__lte=s_dte,use_date__gte=e_dte)
        output = ''
        attendance=set()
        for log in logs:
            attendance.add(log.user.user)


        for u in attendance:
            output += u.username + '\n'

        if output == '':
            status_code = 204 # No content
        else:
            status_code=200 # Content
    else:
        #Don't check the cached results in the database
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

def c_members_connected(request):
    s_dte=datetime.now
    e_dte=s_dte-datetime.timedelta(hour=1)
    logs = UsageLog.objects.filter(use_date__range=[s_dte,e_dte])
    output = ''
    for log in logs:
        output += log.user.username + '\n'

    if output == '':
        status_code = 204 # No content
    else:
        status_code=200 # Content

    return render(request, 'members_connected.html', {'user_list':output},content_type="text/plain",status=status_code)

def unknown_connected(request):
=======
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
import paramiko, base64, pickle, os
from MakerBarManager.presence.models import UserProfilePresence, Device
from paramiko.ssh_exception import AuthenticationException

def members_connected(request):
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201

    rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
    router_address=settings.MAKERBAR_ROUTER_ADDRESS
    router_port = settings.MAKERBAR_ROUTER_PORT
    stdin, stdout, stderr =get_router_mac_addresses(rsa_key,router_address,router_port)

<<<<<<< HEAD
    unknown = set()
=======
    attendance = set()
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201
    for line in stdout:
        router_mac = line[10:27]
        try:
            e = UserProfilePresence.objects.get(device__mac=router_mac)
<<<<<<< HEAD
        except UserProfilePresence.DoesNotExist:
            unknown.add(router_mac)
=======
            attendance.add(e.user)
        except UserProfilePresence.DoesNotExist:
            pass
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201
        except Device.DoesNotExist:
            pass

    output = ''
<<<<<<< HEAD
    for u in unknown:
        output += u + '\n'
=======
    for u in attendance:
        output += u.username + '\n'
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201
        status_code=200 # Content
    if output == '':
        status_code = 204 # No content

<<<<<<< HEAD
    return render(request, 'unknown_connected.html', {'unknown_connected_list':output},content_type="text/plain",status=status_code)
=======
    return render(request, 'members_connected.html', {'user_list':output},content_type="text/plain",status=status_code)
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201

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