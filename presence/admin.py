from MakerBarManager.presence.models import UserProfilePresence, Device,UsageLog
from django.contrib import admin

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 3

class UserProfilePresenceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User' , {'fields': ['user']}),
        ('Social Media Tokens'   ,{'fields':['meetup_id','four_square_token','facebook_token']}),
    ]
    inlines = [DeviceInline]

class UsageLogAdmin(admin.ModelAdmin):
    fields=['user','device','use_date']
    list_display = ('user','device','use_date')

admin.site.register(UserProfilePresence,UserProfilePresenceAdmin)
admin.site.register(UsageLog,UsageLogAdmin)