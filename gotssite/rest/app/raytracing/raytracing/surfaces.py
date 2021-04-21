import numpy as np
import matplotlib.pyplot as plt
from cmath import sqrt

eps = 1e-9

class QuarticOpticalSurface(object):
	"""
	La clase QuarticOpticalSurface permite crear objetos de este tipo los cuales son superficies Cartesianas.
	Estos objetos se defines a partir de los siguientes parametros:
	position: posicion del vertice de la superficie a lo largo del eje z
	n_o: indice de refraccion anterior a la superficie
	n_i: indice de refraccion posterior a la superficie
	z_o: punto rigurosamente estigmatico, objeto puntual
	z_i: punto rigurosamente estigmatico, imagen puntual
	rho_max: maximo valor que toma el parametro rho

	Esta clase define los parametros de forma de la superficie y los almacena en las variables K, c_0, c_1 y b_1
	de esta misma clase.
	"""
	def __init__(self, **kwargs):
		super(QuarticOpticalSurface, self).__init__()
		self.position = kwargs.get('position', 0)
		self.mback, self.mfront = kwargs.get('materials', (None, None))
		self.n_o, self.n_i, self.z_o, self.z_i = kwargs.get('parameters', (None, None, None, None))
		self.rho_max = kwargs.get('rho_max', None)
		self.z_o = self.z_o - self.position
		self.z_i = self.z_i - self.position
		zeta_o = 1.0/self.z_o
		zeta_i = 1.0/self.z_i

		self.G   = (self.n_i**2*zeta_o - self.n_o**2*zeta_i)**2/(self.n_i*self.n_o*(self.n_i*zeta_i - self.n_o*zeta_o)*(self.n_i*zeta_o - self.n_o*zeta_i))
		self.O = (self.n_i*zeta_i - self.n_o*zeta_o)/(self.n_i - self.n_o)
		self.T = zeta_i**2*zeta_o**2*(self.n_i - self.n_o)*(self.n_i + self.n_o)**2/(4*self.n_i*self.n_o*(self.n_i*zeta_o - self.n_o*zeta_i))
		self.S = zeta_i*zeta_o*(self.n_i + self.n_o)*(self.n_i**2*zeta_o - self.n_o**2*zeta_i)/(2*self.n_i*self.n_o*(self.n_i*zeta_o - self.n_o*zeta_i))

		#print('##### Form parameters #####')
		#print('G = {}, O = {}, T = {}, S = {}'.format(self.G, 1/self.O, self.T, self.S))

	def surface_function(self, rho):
		"""
		La funcion surface_function de la clase QuarticOpticalSurface calcula las coordenadas de la superficie para los valores de rho dados. Esta funcion recibe
		como parametro de entrada el valor de rho y retorna las coordenadas (z,r) para ese valor de rho.
		"""
		cvarphi = (self.O + self.T*rho**2)*rho/(1 + self.S*rho**2 + np.sqrt(1 + (2*self.S-self.O**2*self.G)*rho**2))
		varphi = np.arccos(cvarphi)+0j
		z = rho*np.cos(varphi)
		r = rho*np.sin(varphi)
		return np.concatenate(([z.real],[r.real]), axis=0), varphi.real

	def surface_derivative(self,rho,varphi):
		"""
		La funcion surface_derivative de la clase QuarticOpticalSurface permite calcular la derivada dz/drho que es usada para calcular el vector normal a la
		superficie. Esta funcion recibe como parametros de entrada el valor de rho y del algulo varphi, que es el angulo que que hace rho con el eje z, y retorna
		el valor de la derivada.
		"""
		return -2*(self.S*rho**2 - self.O*self.G*rho*np.cos(varphi) + 1)*np.sin(varphi)/(3*self.T*rho**2 - 4*self.S*rho*np.cos(varphi) + self.O*(self.G*np.cos(varphi)**2 + 1))

	def surface_normal(self,rho,varphi):
		"""
		La funcion surface_normal de la clase QuarticOpticalSurface permite calcular la normal a la superficie Cartesiana. Esta funcion recibe como parametro
		de entrada el valor de rho y el angulo que este hace con el eje z, y retorna el vector unitario normal en ese punto sobre la superficie.
		"""
		Dvp = self.surface_derivative
		nz = -(Dvp(rho,varphi)*np.sin(varphi) + rho*np.cos(varphi))/np.sqrt(Dvp(rho,varphi)**2 + rho**2)
		nr =  (Dvp(rho,varphi)*np.cos(varphi) - rho*np.sin(varphi))/np.sqrt(Dvp(rho,varphi)**2 + rho**2)
		if nz > 0:
			nz = -nz
			nr = -nr
		return np.concatenate(([nz.real],[nr.real]), axis=0)

	def form_parameters(self):
		return self.G, self.O, self.T, self.S
	
	def aspherical_coefficients(self):
		A4 = -self.S*(self.G*self.O**2 - self.S)/(2*self.G*self.O)
		A6 = self.S*(self.G*self.O**2*(-3*self.G*self.O**2 - 4*self.O**2 + 6*self.S) + 4*self.O**2*self.S - 4*self.S**2)/(8*self.G*self.O)
		A8 =  5*self.S*(self.G**2*self.O**2*(-2*self.G**2*self.O**4 - 5*self.G*self.O**4 + 6*self.G*self.O**2*self.S - 3*self.O**4 + 12*self.O**2*self.S - 8*self.S**2) + 3*self.G*self.O**2*self.S*(self.O**2 - 4*self.S) + 4*self.G*self.S**3 + 4*self.S**3)/(32*self.G**2*self.O)
		A10 = self.S*(self.G**3*self.O**4*(-35*self.G**3*self.O**6 - 126*self.G**2*self.O**6 + 140*self.G**2*self.O**4*self.S - 147*self.G*self.O**6 + 450*self.G*self.O**4*self.S - 280*self.G*self.O**2*self.S**2 - 56*self.O**6 + 378*self.O**4*self.S - 800*self.O**2*self.S**2 + 280*self.S**3) + 4*self.G**2*self.O**4*self.S*(14*self.O**4 - 105*self.O**2*self.S + 180*self.S**2) - 112*self.G**2*self.O**2*self.S**4 + 168*self.G*self.O**4*self.S**3 - 288*self.G*self.O**2*self.S**4 + 32*self.S**5)/(128*self.G**3*self.O**3)
		A12 = 7*self.S*(self.G**3*self.O**4*(-9*self.G**4*self.O**8 - 42*self.G**3*self.O**8 + 45*self.G**3*self.O**6*self.S - 72*self.G**2*self.O**8 + 196*self.G**2*self.O**6*self.S - 120*self.G**2*self.O**4*self.S**2 - 54*self.G*self.O**8 + 280*self.G*self.O**6*self.S - 490*self.G*self.O**4*self.S**2 + 180*self.G*self.O**2*self.S**3 - 15*self.O**8 + 144*self.O**6*self.S - 560*self.O**4*self.S**2 + 700*self.O**2*self.S**3 - 144*self.S**4) + self.G**2*self.O**4*self.S*(15*self.O**6 - 168*self.O**4*self.S + 600*self.O**2*self.S**2 - 560*self.S**3) + 48*self.G**2*self.O**2*self.S**5 + 8*self.G*self.O**4*self.S**3*(9*self.O**2 - 40*self.S) + 224*self.G*self.O**2*self.S**5 + 64*self.O**2*self.S**5 - 32*self.S**6)/(256*self.G**3*self.O**3)
		A14 = 3*self.S*(self.G**4*self.O**4*(-77*self.G**5*self.O**10 - 440*self.G**4*self.O**10 + 462*self.G**4*self.O**8*self.S - 990*self.G**3*self.O**10 + 2520*self.G**3*self.O**8*self.S - 1540*self.G**3*self.O**6*self.S**2 - 1100*self.G**2*self.O**10 + 5040*self.G**2*self.O**8*self.S - 8064*self.G**2*self.O**6*self.S**2 + 3080*self.G**2*self.O**4*self.S**3 - 605*self.G*self.O**10 + 4500*self.G*self.O**8*self.S - 14112*self.G*self.O**6*self.S**2 + 15680*self.G*self.O**4*self.S**3 - 3696*self.G*self.O**2*self.S**4 - 132*self.O**10 + 1650*self.O**8*self.S - 9600*self.O**6*self.S**2 + 23520*self.O**4*self.S**3 - 18816*self.O**2*self.S**4 + 2464*self.S**5) + 4*self.G**3*self.O**4*self.S*(33*self.O**8 - 495*self.O**6*self.S + 2800*self.O**4*self.S**2 - 5880*self.O**2*self.S**3 + 3360*self.S**4) - 704*self.G**3*self.O**2*self.S**6 + self.G**2*self.O**4*self.S**3*(880*self.O**4 - 6720*self.O**2*self.S + 13440*self.S**2) - 5120*self.G**2*self.O**2*self.S**6 + 1600*self.G*self.O**4*self.S**5 - 3840*self.G*self.O**2*self.S**6 + 768*self.G*self.S**7 + 384*self.S**7)/(1024*self.G**4*self.O**3)
		A16 = self.S*(self.G**5*self.O**6*(-156156*self.G**6*self.O**12 - 1054053*self.G**5*self.O**12 + 1093092*self.G**5*self.O**10*self.S - 2927925*self.G**4*self.O**12 + 7135128*self.G**4*self.O**10*self.S - 4372368*self.G**4*self.O**8*self.S**2 - 4294290*self.G**3*self.O**12 + 18242987*self.G**3*self.O**10*self.S - 27747720*self.G**3*self.O**8*self.S**2 + 10930920*self.G**3*self.O**6*self.S**3 - 3513510*self.G**2*self.O**12 + 23122148*self.G**2*self.O**10*self.S - 64862056*self.G**2*self.O**8*self.S**2 + 68108040*self.G**2*self.O**6*self.S**3 - 17489472*self.G**2*self.O**4*self.S**4 - 1522521*self.G*self.O**12 + 14863422*self.G*self.O**10*self.S - 69360004*self.G*self.O**8*self.S**2 + 144458440*self.G*self.O**6*self.S**3 - 108972864*self.G*self.O**4*self.S**4 + 17489472*self.G*self.O**2*self.S**5 - 273273*self.O**12 + 4215260*self.O**10*self.S - 33022640*self.O**8*self.S**2 + 126088952*self.O**6*self.S**3 - 208005504*self.O**4*self.S**4 + 113008896*self.O**2*self.S**5 - 9993984*self.S**6) + self.G**4*self.O**6*self.S*(273035*self.O**10 - 5149340*self.O**8*self.S + 40512612*self.O**6*self.S**2 - 141184256*self.O**4*self.S**3 + 192580640*self.O**2*self.S**4 - 72648576*self.S**5) + 2498496*self.G**4*self.O**4*self.S**7 + self.G**3*self.O**6*self.S**3*(2338532*self.O**6 - 25912992*self.O**4*self.S + 94086848*self.O**2*self.S**2 - 110036864*self.S**3) + 25945920*self.G**3*self.O**4*self.S**7 + self.G**2*self.O**6*self.S**5*(6712384*self.O**2 - 33582400*self.S) + 35369152*self.G**2*self.O**4*self.S**7 - 3843840*self.G**2*self.O**2*self.S**8 + 4792640*self.G*self.O**4*self.S**7 - 5241600*self.G*self.O**2*self.S**8 + 209664*self.S**9)/(745472*self.G**5*self.O**5)

		return A4, A6, A8, A10, A12, A14, A16

	def cubic_root(self,x):
		if x.real >= 0:
			return x**(1./3.)
		else:
			return -(-x)**(1./3.)

	def solve_quartic(self, A0, A1, A2, A3, A4):
		a, b, c, d, e = A4, A3, A2, A1, A0
		z_1, z_2, z_3, z_4 = None, None, None, None
		if b != 0 and a != 0:
			p = 0.125*(8.*a*c - 3.*b**2)/a**2
			q = 0.125*(b**3 - 4.*a*b*c + 8.*a**2*d)/a**3
			D0 = c**2 - 3.*b*d + 12.*a*e
			D1 = 2.0*c**3 - 9.*b*c*d + 27.*b**2*e + 27.*a*d**2 - 72.*a*c*e

			Q = self.cubic_root(0.5*(D1 + sqrt(D1**2 -4*D0**3)))
			S = 0.5*sqrt(-(2./3.)*p + (Q + D0/Q)/(3.*a))
			
			z_1 = -0.25*b/a - S + 0.5*sqrt(-4.*S**2 - 2.*p + q/S)
			z_2 = -0.25*b/a - S - 0.5*sqrt(-4.*S**2 - 2.*p + q/S)
			z_3 = -0.25*b/a + S + 0.5*sqrt(-4.*S**2 - 2.*p - q/S)
			z_4 = -0.25*b/a + S - 0.5*sqrt(-4.*S**2 - 2.*p - q/S)

			return [z_1, z_2, z_3, z_4]
		else:
			z_1 = 0.5*(-d + np.sqrt(d**2 - 4*c*e))/c
			z_2 = 0.5*(-d - np.sqrt(d**2 - 4*c*e))/c

			return [z_1, z_2]
