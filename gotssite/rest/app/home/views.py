from rest_framework import status
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from rest.app.home.models import Configuration, Menu, MenuItem, MenuItemElement

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
			configuration = Configuration.objects.get(pk=1)
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

		status_code = status.HTTP_200_OK
		response = {
			'success': 'true',
			'status code': status_code,
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user
		}

		return render(request, self.template_name, response)