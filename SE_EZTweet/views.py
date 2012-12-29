from django.shortcuts import redirect
from django.conf import settings
import os, datetime,urllib2, json, random
from time import time
from datetime import datetime, timedelta

def tweet_am_festival(request):
    #[meetup_event_name,event_time,event_duration]=get_current_meetup_event_name()
    tweet_base_url='http://twitter.com/home?status='
    tweet_url='Checking out @MakerBar at the Hoboken Arts and Music Festival. MakerBar.com'
    final_url=tweet_base_url+tweet_url.replace(' ','%20').replace('@','%40').replace('#','%25')

    return redirect(final_url,permanent=False)

def tweet_makerfaire(request):
    #[meetup_event_name,event_time,event_duration]=get_current_meetup_event_name()
    tweet_base_url='http://twitter.com/home?status='
    tweet_url='Checking out @MakerBar at @Makerfaire. MakerBar.com'
    final_url=tweet_base_url+tweet_url.replace(' ','%20').replace('@','%40').replace('#','%25')

    return redirect(final_url,permanent=False)

