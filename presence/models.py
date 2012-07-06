from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201

class UserProfilePresence(models.Model):
    user = models.OneToOneField(User,unique=True)

    def __unicode__(self):
        return self.user.username

class Device(models.Model):
    user = models.ForeignKey(UserProfilePresence)
    name=models.CharField('Device Name',max_length=30)
    mac=models.CharField('MAC Address',max_length=17)

    def __unicode__(self):
<<<<<<< HEAD
        return self.name

class UsageLog(models.Model):
    user = models.ForeignKey(UserProfilePresence)
    device = models.ForeignKey(Device)
    use_date = models.DateTimeField(default=datetime.now)

#   def __unicode__(self):
#        return '%s logged in at %s with %s' % (self.user.username,str(self.dateTime),self.device.name)
=======
        return self.name
>>>>>>> 6ea3eac18435fdb17b193b32605f3e7bee2b0201
