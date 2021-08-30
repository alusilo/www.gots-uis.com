from django.contrib import admin

from apps.simulation.models import Material


class MaterialAdmin(admin.ModelAdmin):
	fields = ['name']

admin.site.register(Material, MaterialAdmin)
