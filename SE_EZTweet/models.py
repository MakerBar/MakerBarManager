from django.db import models

# Create your models here.
class TweetTemplates(models.Model):
    template = models.CharField('TweetTemplate',max_length=140)
    isEventSensitive=models.BooleanField()\

    def __unicode__(self):
        return self.template
