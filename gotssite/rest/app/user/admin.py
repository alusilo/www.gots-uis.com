from django.contrib import admin

from rest.app.user.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
	list_filter = ('email', 'is_active',)
	search_fields = ['email', 'username']

admin.site.register(User, UserAdmin)
