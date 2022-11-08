from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement, Event
from apps.blog.models import Post
from apps.user.models import User
from apps.research.models import ResearchArea


class HomeView(TemplateView):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.first()
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		time_now = timezone.now()
		events = Event.objects.all().order_by('starting_date')[:4]
		events = [event for event in events if event.ending_date > time_now]
		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'carousel_items': Post.objects.all().filter(carousel_item=True),
			'post_list': Post.objects.all().order_by('-created_on')[:5],
			'research_areas': ResearchArea.objects.all(),
			'events': events
		}

		return render(request, self.template_name, response)


class AboutView(TemplateView):
	template_name = "about.html"

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.first()
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user
		}

		return render(request, self.template_name, response)


class PeopleView(TemplateView):
	template_name = "people.html"

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.first()
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		users = User.objects.all().order_by('role')
		user_roles = [user.role for user in users]
		roles = [role for role in User.ROLE_CHOICES if role[0] in user_roles]
		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'users': users,
			'roles': roles
		}

		return render(request, self.template_name, response)
