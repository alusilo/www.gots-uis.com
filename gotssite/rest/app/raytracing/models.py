from django.db import models

class System(models.Model):
	object_height = models.FloatField(default=0)
	aperture_size = models.FloatField()
	aperture_position = models.FloatField()
	wavelength = models.FloatField()

class Surface(models.Model):
	system = models.ForeignKey(System, related_name='surfaces', on_delete=models.CASCADE)
	position = models.FloatField(default=0)
	obj_material = models.CharField(max_length=12)
	img_material = models.CharField(max_length=12)
	obj_position = models.FloatField()
	img_position = models.FloatField()
	max_rho = models.FloatField()

class Material(models.Model):
	name = models.CharField(max_length=12,unique=True)