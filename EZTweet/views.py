from django.shortcuts import redirect
from django.conf import settings
import os, datetime,urllib2, json, random
from time import time
from datetime import datetime, timedelta
from MakerBarManager.EZTweet.models import TweetTemplates

def tweet_event_fun(request):
    phrases_event_name=TweetTemplates.objects.filter(isEventSensitive=True)
    phrases_no_event_name=TweetTemplates.objects.filter(isEventSensitive=False)

    [meetup_event_name,event_time,event_duration]=get_current_meetup_event_name()

    tweet_base_url='http://twitter.com/home?status='
    if not (meetup_event_name==''):
        reponse_id=int(random.random()*phrases_no_event_name.count())
        tweet_url=(phrases_event_name[reponse_id].template) % meetup_event_name
    else:
        reponse_id=int(random.random()*phrases_event_name.count())
        tweet_url=phrases_no_event_name[reponse_id].template

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