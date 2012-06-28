from django.db import models
from django.contrib.auth.models import User

class UserProfilePresence(models.Model):
    user = models.OneToOneField(User,unique=True)

    def __unicode__(self):
        return self.user.username

class Device(models.Model):
    user = models.ForeignKey(UserProfilePresence)
    name=models.CharField('Device Name',max_length=30)
    mac=models.CharField('MAC Address',max_length=17)

    def __unicode__(self):
        return self.name