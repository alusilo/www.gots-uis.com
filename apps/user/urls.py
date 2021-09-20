from django.urls import path
from apps.user.views import UserDetail

urlpatterns = [
    path('<pk>/', UserDetail.as_view(), name='user_detail'),
]
