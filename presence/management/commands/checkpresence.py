from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from presence.models import UserProfilePresence, Device,UsageLog
from datetime import datetime
from time import time
from django.conf import settings
import paramiko, base64, pickle, os, urllib,urllib2, json, httplib
from paramiko.ssh_exception import AuthenticationException

class Command(BaseCommand):

    def handle(self, *args, **options):
        rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
        router_address=settings.MAKERBAR_ROUTER_ADDRESS
        router_port = settings.MAKERBAR_ROUTER_PORT
        stdin, stdout, stderr =self.get_router_mac_addresses(rsa_key,router_address,router_port)
        print stdout
        for line in stdout:
            router_mac = line[10:27]
            try:
                e = UserProfilePresence.objects.get(device__mac=router_mac)
                meetup_id=e.meetup_id
                dev = Device.objects.get(mac=router_mac)
                u=UsageLog(user=e,device=dev)
                u.save()

                #checkin meetup members
                event_id,event_time=self.get_next_meetup_event()

                if not self.is_member_checked_in(event_id,meetup_id):
                    self.check_in_meetup_member(event_id,event_time,meetup_id)
                    print event_id, event_time, meetup_id, e.user

            except UserProfilePresence.DoesNotExist:
                pass
            except Device.DoesNotExist:
                pass

    def get_router_mac_addresses(self,rsa_key,router_address,router_port):
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
            print "Authentication Excpetion"


        return stdin, stdout, stderr

    def get_next_meetup_event(self):
        #Meetup Event ID
        g_meetup=urllib2.urlopen('https://api.meetup.com/2/events.json/?group_urlname=MakerBar&sign=true&venue_id=6693352&status=upcoming&key=676e1e5f20b623b131e2e4a553b7b41')
        status_code=g_meetup.getcode()
        if status_code==200:
            j_meetup=json.load(g_meetup)
            event_id=j_meetup['results'][0]['id']
            event_time=j_meetup['results'][0]['time']
        else:
            status_code=204

        return event_id,event_time

    def check_in_meetup_member(self,event_id,event_time, meetup_id):
        clk=0
        clk=time()*1000 #adjust for epoch timestamp in milliseconds
        event_duration=10800000 #meetup events assume a 3 hour duration
        meetup_key='676e1e5f20b623b131e2e4a553b7b41'

        if clk>=event_time and clk<=event_time+event_duration:
            data =urllib.urlencode({"event_id": event_id,"attendee_member_id": meetup_id,"key":meetup_key})
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = httplib.HTTPConnection('api.meetup.com')
            conn.request("POST", "/2/checkin", data, headers)
            response = conn.getresponse()
            print response.status, response.reason

    def is_member_checked_in(self, event_id, meetup_id):
        checked_in=False
        url=('https://api.meetup.com/2/checkins?key=676e1e5f20b623b131e2e4a553b7b41&sign=true&member_id=%s&event_id=%s') % (meetup_id,event_id)

        g_meetup=urllib2.urlopen(url)
        status_code=g_meetup.getcode()
        if status_code==200:
            j_meetup=json.load(g_meetup)
            checked_in=(len(j_meetup['results'])!=0)
        else:
            status_code=204
        print checked_in
        return checked_in

    def check_in_foursquare_member(self,event_time,foursquare_id):
        foursquare_client_id='EXXD5BRDFVYTSEQBKMQOPFV5RDVYQ1LY3U5U5QKSTM05MJBE'
        foursquare_client_secret='ZBO5UP151MR4JFF03SVHMUA00D0DHC3G14DY2MGRI5ERN5VO'

