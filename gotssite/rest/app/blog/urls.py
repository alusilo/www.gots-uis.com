from django.urls import path

from rest.app.blog.views import PostList, PostDetail

# Create your urls here.
urlpatterns = [
	path('', PostList.as_view(), name='posts'),
	path('<slug:slug>/', PostDetail.as_view(), name='post_detail')
]