from django.contrib import admin

from rest.app.home.models import Configuration


class ConfigurationAdmin(admin.ModelAdmin):
    fields = ['group_name', 'group_logo', 'total_items_carousel', 'admin_name', 'admin_email']

admin.site.register(Configuration, ConfigurationAdmin)