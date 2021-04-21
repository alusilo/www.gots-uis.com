import numpy as np
import matplotlib.pyplot as plt	

class Ray(object):
	"""
	La clase Ray es una clase que define objetos de tipo Ray, los cuales representan rayos. Este tipo de objetos se definen a partir de los siguientes parametros:
	slope: pendiente que hace el rayo con el eje z
	origin: coordenadas iniciales desde donde se origina el rayo
	"""
	def __init__(self, **kwargs):
		super(Ray, self).__init__()
		#self.wl = kwargs.get('wavelength', 0)
		self.slope = kwargs.get('slope', 0)
		self.origin = kwargs.get('origin', (0,0))
		self.wl = kwargs.get('wavelength', None)
		self.color = kwargs.get('color', None)

	def ray_function(self,z):
		"""
		La funcion ray_funtion que pertenece a la clase Ray permite calcular la coordenada r del rayo. Esta funcion recibe como parametro de entrada el valor de
		la coordenada z y retorna el valor de la coordenada r.
		"""
		z_o, r_o = self.origin
		b = r_o - self.slope*z_o
		return self.slope*z + b
