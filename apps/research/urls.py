from django.urls import path

from apps.research.views import ResearchAreaList, ResearchAreaDetail

# Create your urls here.
urlpatterns = [
	path('', ResearchAreaList.as_view(), name='researcharea'),
	path('<slug:slug>/', ResearchAreaDetail.as_view(), name='researcharea_detail')
]