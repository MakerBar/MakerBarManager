from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^SupplyRequest/$', 'MakerBarManager.SupplyRequest.views.home', name='home'),
    url(r'^presence/members_connected/$', 'MakerBarManager.presence.views.members_connected', name='members_connected'),
    url(r'^presence/members_connected/(?P<lookback>\w{1,50})/$', 'MakerBarManager.presence.views.members_connected', name='members_connected'),
    url(r'^presence/who_is_connected/$', 'MakerBarManager.presence.views.who_is_connected', name='who_is_connected'),
    url(r'^presence/unknown_connected/$', 'MakerBarManager.presence.views.unknown_connected', name='unknown_connected'),
    url(r'^presence/member_data/$', 'MakerBarManager.presence.views.post_member_status', name='post_member_status'),
    url(r'^social_numbers/$','MakerBarManager.Social_Media_Tracker.views.social_numbers', name='social_numbers'),
    #url(r'^tweet_the_fun/$','MakerBarManager.presence.views.tweet_event_fun', name='tweet_event_fun'),
    url(r'^supply_request/$','MakerBarManager.SupplyRequest.views.order_request', name='order_request'),
    url(r'^tweet_the_fun/$','MakerBarManager.EZTweet.views.tweet_event_fun',name='ez_tweet'),
    url(r'^tweet_am_festival/$','MakerBarManager.SE_EZTweet.views.tweet_am_festival',name='tweet_am_festival'),
    url(r'^tweet_makerfaire/$','MakerBarManager.SE_EZTweet.views.tweet_makerfaire',name='tweet_makerfaire'),
    #url(r'^MakerBarManager/', include('MakerBarManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment these two lines to enable your static files on PythonAnywhere
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

