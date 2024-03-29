from django.shortcuts import render
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement
from apps.blog.models import Post, Comment

from apps.blog.forms import CommentForm


# Create your views here.
class PostList(generic.ListView):
	template_name = 'post_list.html'

	def get(self, request, *args, **kwargs):
		object_list = Post.objects.filter(status=1).order_by('-created_on')
		paginator = Paginator(object_list, 5)
		page = request.GET.get('page')
		
		try:
			post_list = paginator.page(page)
		except PageNotAnInteger:
			post_list = paginator.page(1)
		except EmptyPage:
			post_list = paginator.page(paginator.num_pages)

		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.get(pk=1)
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'post_list': post_list,
			'page': page
		}

		return render(request, self.template_name, response)

class PostDetail(generic.DetailView):
	model = Post
	template_name = 'post_detail.html'

	def get(self, request, *args, **kwargs):
		slug = self.kwargs.get("slug")
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.get(pk=1)
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		post = Post.objects.get(slug=slug)
		comments = Comment.objects.filter(post=post).filter(active=True)
		comment_form = CommentForm()
		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'post': post,
			'comments': comments,
			'comment_form': comment_form
		}

		return render(request, self.template_name, response)

	def post(self, request, slug, *args, **kwargs):
		post = Post.objects.get(slug=slug)
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()

		comments = Comment.objects.filter(post=post).filter(active=True)

		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.get(pk=1)
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user,
			'post': post,
			'comments': comments,
			'comment_form': comment_form
		}

		return render(request, self.template_name, response)
