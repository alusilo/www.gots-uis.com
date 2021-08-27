from django.urls import path

from apps.simulation.views import SimulationList, RaytracingSimulation

# Create your urls here.
urlpatterns = [
	path('', SimulationList.as_view(), name='simulations'),
	path('raytracing/', RaytracingSimulation.as_view(), name='raytracing_simulation'),
	#path('<slug:slug>/', ResearchAreaDetail.as_view(), name='researcharea_detail'),
	#path('publications/<slug:slug>/', PublicationDetail.as_view(), name='publication_detail')
]