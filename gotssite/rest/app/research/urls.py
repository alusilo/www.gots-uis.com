from django.urls import path

from rest.app.research.views import ResearchAreaList, ResearchAreaDetail

# Create your urls here.
urlpatterns = [
	path('', ResearchAreaList.as_view(), name='researcharea'),
	path('<slug:slug>/', ResearchAreaDetail.as_view(), name='researcharea_detail')
]