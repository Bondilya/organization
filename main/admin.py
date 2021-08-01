from django.contrib import admin
from .models import *


class VolunteersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)
    fields = (('first_name', 'last_name'), 'email', 'hours', 'status', 'image', 'description', 'username', 'is_active')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_volunteers', 'date', 'hours', 'is_over')
    list_display_links = ('name',)
    search_fields = ('name', 'date')
    list_filter = ('is_over',)


admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participant)
admin.site.register(Waste)
# Register your models here.
