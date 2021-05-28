from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement
from apps.blog.models import Post
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

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'carousel_items': Post.objects.all().filter(carousel_item=True),
			'research_areas': ResearchArea.objects.all()
		}

		return render(request, self.template_name, response)
		