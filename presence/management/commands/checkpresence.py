from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from presence.models import UserProfilePresence, Device,UsageLog
from datetime import datetime
from django.conf import settings
import paramiko, base64, pickle, os
from paramiko.ssh_exception import AuthenticationException

class Command(BaseCommand):

    def handle(self, *args, **options):
        rsa_key=settings.MAKERBAR_ROUTER_RSA_KEY
        router_address=settings.MAKERBAR_ROUTER_ADDRESS
        router_port = settings.MAKERBAR_ROUTER_PORT
        stdin, stdout, stderr =self.get_router_mac_addresses(rsa_key,router_address,router_port)

        for line in stdout:
            router_mac = line[10:27]
            try:
                e = UserProfilePresence.objects.get(device__mac=router_mac)
                dev = Device.objects.get(mac=router_mac)
                u=UsageLog(user=e,device=dev)
                u.save()
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
            stdin=''
            stdout=''
            stderr=''
            pass

        return stdin, stdout, stderr