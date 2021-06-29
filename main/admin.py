from django.contrib import admin
from .models import *


class VolunteersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('status',)
    fields = (('first_name', 'last_name'), 'email', 'hours', 'status', 'image', 'description', 'username', 'is_active')


admin.site.register(Volunteer, VolunteersAdmin)
admin.site.register(Event)
# Register your models here.
