from django.shortcuts import render
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement
from apps.user.models import User


# Create your views here.
class UserDetail(generic.DetailView):
	template_name = 'user_detail.html'

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get("pk")
		
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

		try:
			user_info = User.objects.get(pk=pk)
			response = {
				'success': 'true',
				'message': 'Configuration data fetched successfully',
				'data': {
					'configuration': configuration,
					'menu': menu_data
				},
				'user': user,
				'user_info': user_info,
			}

			return render(request, self.template_name, response)
		except ValidationError:
			raise Http404