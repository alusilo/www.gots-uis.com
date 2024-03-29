from django.urls import path
from apps.home.views import HomeView, AboutView, PeopleView

urlpatterns = [
    path('', HomeView.as_view()),
    path('about/', AboutView.as_view(), name='about'),
    path('people/', PeopleView.as_view()),
]
