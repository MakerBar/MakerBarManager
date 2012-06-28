from MakerBarManager.presence.models import UserProfilePresence, Device
from django.contrib import admin

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 3

class UserProfilePresenceAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    ('Request Information' , {'fields': ['username']}),
    #]
    inlines = [DeviceInline]


admin.site.register(UserProfilePresence,UserProfilePresenceAdmin)
