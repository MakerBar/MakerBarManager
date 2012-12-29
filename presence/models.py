from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfilePresence(models.Model):
    user = models.OneToOneField(User,unique=True)
    #uid = models.IntegerField('UID')
    #membership_expiration=models.DateTimeField()
    meetup_id = models.CharField('Meetup ID',max_length=10)
    four_square_token = models.CharField('Foursquare Token',max_length=50)
    facebook_token = models.CharField('Facebook Token',max_length=50)

    def __unicode__(self):
        return self.user.username

class Device(models.Model):
    user = models.ForeignKey(UserProfilePresence)
    name=models.CharField('Device Name',max_length=30)
    mac=models.CharField('MAC Address',max_length=17)

    def __unicode__(self):
        return self.name

class UsageLog(models.Model):
    user = models.ForeignKey(UserProfilePresence)
    device = models.ForeignKey(Device)
    use_date = models.DateTimeField(default=datetime.now)

#   def __unicode__(self):
#        return '%s logged in at %s with %s' % (self.user.username,str(self.dateTime),self.device.name)