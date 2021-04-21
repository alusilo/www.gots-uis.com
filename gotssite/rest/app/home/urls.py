from django.conf.urls import url
from rest.app.home.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
]