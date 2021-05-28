from django.db import models
from apps.user.models import User
from django.template.defaultfilters import truncatechars

STATUS = (
	(0, "Draft"),
	(1, "Publish")
)
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	abstract = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='static/img/blog', default='/static/img/blog/default.jpg')
	updated_on = models.DateTimeField(auto_now=True)
	content = models.TextField(blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS, default=0)
	carousel_item = models.BooleanField('show item in carousel', default=False)

	class Meta:
		ordering = ['-created_on']

	@property
	def short_description(self):
		return truncatechars(self.abstract, 200)

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)

	class Meta:
		ordering = ['created_on']

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)