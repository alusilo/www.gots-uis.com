from django.db import models

class Configuration(models.Model):
	group_name = models.CharField(max_length=45)
	admin_name = models.CharField(max_length=45)
	admin_email = models.CharField(max_length=45)
	group_logo = models.ImageField(upload_to='static', default='static/logo.png')

	def save(self):
		# count will have all of the objects from the Aboutus model
		count = Configuration.objects.all().count()
		# this will check if the variable exist so we can update the existing ones
		save_permission = Configuration.has_add_permission(self)
		# if there's more than two objects it will not save them in the database
		if count < 2:
			super(Configuration, self).save()
		elif save_permission:
			super(Configuration, self).save()

	def has_add_permission(self):
		return Configuration.objects.filter(id=self.id).exists()
