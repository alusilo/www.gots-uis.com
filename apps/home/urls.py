from django.urls import path
from apps.home.views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view()),
    path('about/', AboutView.as_view()),
]