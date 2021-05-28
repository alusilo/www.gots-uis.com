from django.conf.urls import url
from apps.home.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
]