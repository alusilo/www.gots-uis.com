from rest_framework import status
from django.shortcuts import render
from django.views.generic import TemplateView
from rest.app.home.models import Configuration

class HomeView(TemplateView):
	template_name = "index.html"
	def get(self, request, *args, **kwargs):
		configuration = Configuration.objects.all()
		status_code = status.HTTP_200_OK
		if len(configuration) == 0:
			response = {
				'success': 'true',
				'status code': status_code,
				'message': 'Configuration data fetched successfully',
				'data': {
					'configuration': None
				}
			}
		else:
			response = {
				'success': 'true',
				'status code': status_code,
				'message': 'Configuration data fetched successfully',
				'data': {
					'configuration': configuration[0]
				}
			}

		return render(request, self.template_name, response)