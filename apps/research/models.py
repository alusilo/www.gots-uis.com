from django.db import models

from apps.user.models import User

# Create your models here.
class ResearchArea(models.Model):
	area = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField()
	image = models.ImageField(upload_to='research/img')
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
	slug = models.SlugField(max_length=200, unique=True)
	abstract = models.TextField()
	full_description = models.TextField(blank=True, null=True)
	journal = models.CharField(max_length=200)
	pub_date = models.DateField()
	pdf_file = models.FileField(upload_to='research/publications/pdf', blank=True, null=True)
	image = models.ImageField(upload_to='research/publications/img')
	doi = models.URLField()

	def __str__(self):
		return self.title

