from django.db import models

class Configuration(models.Model):
	group_name = models.CharField(max_length=45)
	admin_name = models.CharField(max_length=45)
	admin_email = models.CharField(max_length=45)
	group_logo = models.ImageField(upload_to='static', default='static/img/logo.png')

	def __str__(self):
		return "Initial Configuration - %s" % self.group_name


class Menu(models.Model):
	name = models.CharField(max_length=45)

	def __str__(self):
		return self.name

class MenuItem(models.Model):
	name = models.CharField(max_length=45)
	url = models.URLField(max_length=200)
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

	def __str__(self):
		return "%s > %s" % (self.menu.name, self.name)

class MenuItemElement(models.Model):
	name = models.CharField(max_length=45)
	url = models.URLField(max_length=200, blank=True, null=True)
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

	def __str__(self):
		return "%s > %s > %s" % (self.menu_item.menu.name, self.menu_item.name, self.name)
