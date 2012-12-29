from django.shortcuts import render, redirect
from django.conf import settings
import paramiko, base64, pickle, os, datetime,urllib2, json, random
from time import time
from datetime import datetime, timedelta
from MakerBarManager.presence.models import UserProfilePresence, Device, UsageLog
from paramiko.ssh_exception import AuthenticationException
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
    elif int_lookback==0:
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
    else:
        status_code=204

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

    rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
    router_address=settings.MAKERBAR_ROUTER_ADDRESS
    router_port = settings.MAKERBAR_ROUTER_PORT
    stdin, stdout, stderr =get_router_mac_addresses(rsa_key,router_address,router_port)

    unknown = set()
    for line in stdout:
        router_mac = line[10:27]
        try:
            e = UserProfilePresence.objects.get(device__mac=router_mac)
        except UserProfilePresence.DoesNotExist:
            unknown.add(router_mac)
        except Device.DoesNotExist:
            pass

    output = ''
    for u in unknown:
        output += u + '\n'
        status_code=200 # Content
    if output == '':
        status_code = 204 # No content

    return render(request, 'unknown_connected.html', {'unknown_connected_list':output},content_type="text/plain",status=status_code)

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

def tweet_event_fun(request):
    phrases_event_name=['Visiting @MakerBar for %s and I am having a great time! Makerbar.com',
                        'I am visiting @MakerBar for %s and learning a ton! Makerbar.com',
                        'Checking out @MakerBar for %s, now I don\'t want to leave! Makerbar.com',]
    phrases_no_event_name=[ 'Visiting @MakerBar and having a great time! Makerbar.com',
                            'I am visiting @MakerBar and learning a ton! Makerbar.com',
                            'Checking out @MakerBar, now I don\'t want to leave! Makerbar.com',]

    reponse_id=int(random.random()*len(phrases_event_name))

    [meetup_event_name,event_time,event_duration]=get_current_meetup_event_name()

    tweet_base_url='http://twitter.com/home?status='
    if not (meetup_event_name==''):
        tweet_url=(phrases_event_name[reponse_id]) % meetup_event_name
    else:
        tweet_url=phrases_no_event_name[reponse_id]

    final_url=tweet_base_url+tweet_url.replace(' ','%20').replace('@','%40').replace('#','%25')

    return redirect(final_url,permanent=False)

def get_current_meetup_event_name():
    #Meetup Event Name

    g_meetup=urllib2.urlopen('https://api.meetup.com/2/events.json/?group_urlname=MakerBar&sign=true&venue_id=6693352&status=upcoming&key=676e1e5f20b623b131e2e4a553b7b41')
    status_code=g_meetup.getcode()
    if status_code==200:
        j_meetup=json.load(g_meetup)
        event_id=j_meetup['results'][0]['id']
        event_name=j_meetup['results'][0]['name']
        event_time=j_meetup['results'][0]['time']
        event_duration=10800000 #meetup events assume a 3 hour duration
    else:
        status_code=204

    clk=time()*1000 #adjust for epoch timestamp in milliseconds

    if not (clk>=event_time and clk<=event_time+event_duration):
        event_name=''

    return event_name,event_time,event_duration

#Not safe must check for authentication
@csrf_exempt
def post_member_status(request):
    output=''
    #for key in request.POST:
    #    value = request.POST[key]
    #    output+= key + ':'+value + ', '

    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username, password=password)
    user=None
    if user is not None:
        if user.is_staff:
            login(request,user)
            #success: post
            if request.method=='POST':

                status_code=200
            else:
                status_code=204

            logout(request)
        else:
            #Failure: incorrect permissions
            status_code=401
    else:
        #Failures: invalid login
        status_code=200



    return render(request, 'who_is_connected.html',{'connected_list':output},content_type='application/JSON',status=status_code)


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

