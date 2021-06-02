from django.db import models
from apps.user.models import User
from django.template.defaultfilters import truncatechars
from django.conf import settings

from apps.blog.storage import OverwriteStorage

import uuid

STATUS = (
	(0, "Draft"),
	(1, "Publish")
)

def post_image_filename(instance, file):
	filename, extension = file.split('.')
	return 'blog/{}.{}'.format(instance.pk, extension)

# Create your models here.
class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField('Título', max_length=200, unique=True)
	slug = models.SlugField('Slug', max_length=200, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	abstract = models.TextField('Resumen', blank=True, null=True)
	image = models.ImageField('Imagen (1200x400)', upload_to=post_image_filename, storage=OverwriteStorage())
	updated_on = models.DateTimeField('Fecha última actualización', auto_now=True)
	content = models.TextField('Contenido', blank=True, null=True)
	created_on = models.DateTimeField('Fecha de creación', auto_now_add=True)
	status = models.IntegerField('Estado', choices=STATUS, default=0)
	carousel_item = models.BooleanField('Mostrar en la página de inicio', default=False)

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