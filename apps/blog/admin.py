from django.contrib import admin

from apps.blog.models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'status', 'created_on', 'carousel_item')
	list_filter = ('status',)
	search_fields = ['title', 'content']
	prepopulated_fields = {'slug': ('title',)}

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(author=request.user)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'post', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments']

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(post__author=request.user)

	def approve_comments(self, request, queryset):
		queryset.update(active=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
