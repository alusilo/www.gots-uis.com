from django.db import models

from apps.user.models import User

# Create your models here.
class ResearchArea(models.Model):
	area = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField()
	image = models.ImageField(upload_to='static/img/research', default='/static/img/research/default.jpg')
	content = models.TextField(blank=True, null=True)
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return self.area

class Publication(models.Model):
	title = models.CharField(max_length=200)
	author = models.ManyToManyField(User)
	area = models.ForeignKey(ResearchArea, on_delete=models.CASCADE)
	abstract = models.TextField()
	full_description = models.TextField(blank=True, null=True)
	journal = models.CharField(max_length=200)
	pub_date = models.DateField()
	pdf_file = models.FileField(upload_to='static/img/research/publications', blank=True, null=True)
	image = models.ImageField(upload_to='static/img/research/publications', default='/static/img/research/publications/default.jpg')
	doi = models.URLField()

	def __str__(self):
		return self.title

