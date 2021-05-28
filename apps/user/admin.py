from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from apps.user.models import User

# Register your models here.
class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'username')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise ValidationError("Password doesn't match")
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'is_active', 'is_superuser')

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
	fieldsets = (
		(None, {'fields': ('email', 'username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'school', 'description', )}),
		('Permissions', {'fields': ('groups', 'is_superuser', 'is_staff', 'is_active')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)
	list_filter = ('email', 'is_active',)
	search_fields = ['email', 'username']
	ordering = ('email',)
	fielter_horizontal = ()

admin.site.register(User, UserAdmin)
# admin.site.register(Group)