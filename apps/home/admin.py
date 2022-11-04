from django.contrib import admin

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement, SeminarEvent


class ConfigurationAdmin(admin.ModelAdmin):
	fields = ['group_name', 'about', 'group_logo', 'group_banner', 'admin_name', 'admin_email']

	def has_add_permission(self, request):
		count = Configuration.objects.all().count()
		
		if count == 0:
			return True

		return False


class MenuAdmin(admin.ModelAdmin):
	fields = ['name']

	def has_add_permission(self, request):
		count = Menu.objects.all().count()
		
		if count == 0:
			return True

		return False


class MenuItemAdmin(admin.ModelAdmin):
	fields = ['name', 'url', 'menu']


class MenuItemElementAdmin(admin.ModelAdmin):
	list_display = ('name', 'menu_item', 'url')
	list_filter = ('menu_item',)
	fields = ['name', 'url', 'menu_item']


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuItemElement, MenuItemElementAdmin)
admin.site.register(SeminarEvent)
