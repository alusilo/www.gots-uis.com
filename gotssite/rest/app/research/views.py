from rest_framework import status
from django.shortcuts import render
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from rest.app.home.models import Configuration, Menu, MenuItem, MenuItemElement
from rest.app.research.models import ResearchArea

# Create your views here.
class ResearchAreaList(generic.ListView):
	template_name = 'researcharea_list.html'

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
			'user': user,
			'researcharea_list': ResearchArea.objects.all().order_by('-created_on')
		}

		return render(request, self.template_name, response)

class ResearchAreaDetail(generic.DetailView):
	template_name = 'researcharea_detail.html'

	def get(self, request, *args, **kwargs):
		slug = self.kwargs.get("slug")
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
		researcharea = ResearchArea.objects.get(slug=slug)
		response = {
			'success': 'true',
			'status code': status_code,
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'researcharea': researcharea,
		}

		return render(request, self.template_name, response)
