from django.shortcuts import render
from django.conf import settings
import os, re,urllib2, json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import mechanize

def social_numbers(request):


    #meetup
    g_meetup=urllib2.urlopen('https://api.meetup.com/groups.json/?group_urlname=MakerBar&fields=members&key=676e1e5f20b623b131e2e4a553b7b41')
    status_code=g_meetup.getcode()
    if status_code==200:
        j_meetup=json.load(g_meetup)
        num_meetup_members=int(j_meetup['results'][0]['members'])
    else:
        status_code=204

    #twitter
    g_twitter=urllib2.urlopen('http://api.twitter.com/1/followers/ids.json?screen_name=MakerBar')
    status_code=g_twitter.getcode()
    if status_code==200:
        j_twitter=json.load(g_twitter)
        num_twitter_followers=len(j_twitter['ids'])
    else:
        status_code=204

    #google groups
    br = mechanize.Browser()
    response = br.open("https://groups.google.com/group/makerbar?hl=en&noredirect=true")
    rg = re.compile('.*?(Members).*?(\\d+)',re.IGNORECASE|re.DOTALL)
    m = rg.search(response.read())
    if m:
        num_google_groups=int(m.group(2))
    else:
        num_google_groups=-999

    br.close()

    #membership
    num_members = len(User.objects.exclude(username__icontains='_Admin'))

    #output=json.dumps('{meetup: %d,google_group : %d,twitter : %d,members :  %d}' % (num_meetup_members,-999, num_twitter_followers,num_members), separators=(',',':'))
    output='{"meetup" : %d,"google_group" : %d,"twitter" : %d,"members" :  %d}' % (num_meetup_members,num_google_groups, num_twitter_followers,num_members)
    #for u in attendance:z
    #    output += u.username + '\n'
    #    status_code=200 # Content
    #if output == '':
    #    status_code = 204 # No content

    return render(request, 'social_numbers.html', {'parem_list':output},content_type="application/json",status=status_code)