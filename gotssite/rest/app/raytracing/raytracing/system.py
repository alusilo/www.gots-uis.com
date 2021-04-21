import numpy as np
import matplotlib.pyplot as plt	
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from quartic_solver import fqs

class QuarticOpticalSystem(object):
	"""
	La clase QuarticOpticalSystem define un sistema optico conformado por superficies Cartesianas mediante los siguientes parametros:
	aperture_position: apertura maxima del sistema
	aperture_size: posicion de la apertura (valido solamente valores negativos)
	image_position: posicion a lo largo del eje z en donde se obtendra la imagen
	"""
	def __init__(self, **kwargs):
		super(QuarticOpticalSystem, self).__init__()
		self.aperture_position = kwargs.get('aperture_position', 0)
		self.aperture_size = kwargs.get('aperture_size', 0)
		self.entrance_position = None
		self.entrance_size = None
		self.exit_position = None
		self.exit_size = None
		self.image_position = kwargs.get('image_position', 0)
		self.object_height = kwargs.get('object_height', False)
		self.rays_backward = kwargs.get('rays_backward', False)
		self.sphere_radius = kwargs.get('sphere_radius', False)
		self.surface_number = 0
		self.rays_number = 0
		self.surfaces = []
		self.rays = []
		self.rays_paths = []
		self.incident_vector = []
		self.distortion = []
		self.image_tras = []
		self.z_o = 0
		self.z_i = 0
		self.rho_max = []
		self.field_curvature = 0
		self.image_height = 0
		self.magnification = 0

	def add_surface(self,obj):
		"""
		La funcion add_surface de la clase QuarticOpticalSystem agrega superficies Cartesianas al sistema,
		recibe como parametro de entrada un objeto de tipo QuarticOpticalSurface, el cual es almacenado en
		la variable surfaces que pertenece a la clase QuarticOpticalSystem. Aqui mismo es definido el rango
		maximo de valores para rho de acuerdo al valor maximo de la apertura, como cada superficie tiene
		diferente curvatura esto hace que cada una de ellas tenga un valor distinto de rho para un valor unico
		y maximo de distancia transversal con respecto al eje z.
		"""
		if self.surface_number == 0:
			self.z_o = obj.z_o + obj.position
		self.z_i = obj.z_i + obj.position
		self.surfaces.append(obj)
		self.surface_number = self.surface_number + 1
		r = self.aperture_size
		Q0 = r**2*(obj.G**2*obj.O**2*r**2 + 4)/(obj.G**2*obj.O**2)+0j
		Q2 = -2*(obj.G**2*obj.O**2*r**2 + obj.G*obj.O**2*r**2 - 4*obj.S*r**2 + 2)/(obj.G**2*obj.O**2)+0j
		Q4 = (obj.G**2*obj.O**2 + 2*obj.G*obj.O**2 + 2*obj.S**2*r**2 - 8*obj.S + obj.O**2)/(obj.G**2*obj.O**2)+0j
		Q6 = -2*obj.S**2*(obj.G - 1)/(obj.G**3*obj.O**2)+0j
		Q8 = obj.S**4/(obj.G**4*obj.O**4)+0j

		self.rho_max.append(obj.rho_max)

	def add_lens(self,obj):
		self.surfaces.append(obj.surfa)
		self.surface_number = self.surface_number + 1
		self.surfaces.append(obj.surfb)
		self.surface_number = self.surface_number + 1

	def add_ray(self,obj):
		"""
		La funcion add_ray de la clase QuarticOpticalSystem agrega rayos al sistema, recibe como parametro de entrada
		un objeto de tipo Ray, el cual es almacenado en la variable rays de la clase QuarticOpticalSystem. Adicionalmente,
		en las variables rays_paths e incident_vector, de esta misma clase, son agregados espacios para su uso en los calculos
		del trazado de rayos.
		"""
		self.rays.append(obj)
		self.rays_number = self.rays_number + 1
		self.rays_paths.append([[],[]])
		self.incident_vector.append([[],[]])

	def refracted_unit_vector(self,no,n,u,N):
		"""
		La funcion refracted_unit_vector de la clase QuarticOpticalSystem calcula el vector unitario refractado por una superficie mediante el uso de la
		forma vectorial de la ley de Snell-Descartes. Esta funcion recibe como parametros de entrada los indices de refraccion anterior y posterior (no, n), el
		vector unitario incidente (u) y el vector unitario normal a la superficie (N), y retorna el vector unitario refractado.
		"""
		r = no/n
		Nz,Nr = N
		uz,ur = u
		Nu  = (Nz*uz+Nr*ur) # N.u
		Nxu = (Nz*ur-Nr*uz) # Nxu
		kn  = (r*Nu + np.sqrt(1 - r**2*Nxu**2))
		return (r*uz-kn*Nz, r*ur-kn*Nr)

	def system_aperture(self):
		d_img = self.aperture_position
		h_img = self.aperture_size
		g = 1
		d_obj = None
		for k in range(self.surface_number):
			s = self.surfaces[self.surface_number-1-k]
			if s.position < self.aperture_position:
				d = s.O + (s.n_i/s.n_o)*(1/(d_img-s.position) - s.O)
				d_obj = s.position + 1/d
				g *= np.abs((s.n_o/s.n_i)*(d_img-s.position)/(d_obj-s.position))
				d_img = d_obj

		if d_obj == None: d_obj = self.aperture_position
		
		self.entrance_size = h_img/g
		self.entrance_position = d_obj

		d_obj = self.aperture_position
		h_obj = self.aperture_size
		g = 1
		d_img = None
		for k in range(self.surface_number):
			s = self.surfaces[k]
			if s.position > self.aperture_position:
				d = s.O + (s.n_o/s.n_i)*(1/(d_obj-s.position) - s.O)
				d_img = s.position + 1/d
				g *= np.abs((s.n_o/s.n_i)*(d_img-s.position)/(d_obj-s.position))
				d_obj = d_img

		if d_img == None: d_img = self.aperture_position

		self.exit_size = h_obj*g
		self.exit_position = d_img
		
		return self.entrance_size, self.entrance_position, self.exit_size, self.exit_position

	def calculate(self):
		"""
		La funcion calculate de la clase QuarticOpticalSystem calcula los puntos de interseccion de cada uno de los rayos que
		acceden al sistema con cada una de las superfcies que lo componen. Esta funcion no recive parametros de entrada y no
		retorna ningun valor.
		"""

		i=0
		for ray in self.rays:
			# puntos de origen del rayo con respecto al origen de coordenadas
			z_o, r_o = ray.origin
			# se agregan los puntos iniciales de los rayos a la variable rays_paths
			self.rays_paths[i][0].append(z_o)
			self.rays_paths[i][1].append(r_o)
			cost = 0
			opl = []
			n_i = 0
			# pendiente del rayo
			m = ray.slope
			# calculo del vector unitario incidente
			incident = (np.cos(np.arctan(m)),np.sin(np.arctan(m)))
			for surface in self.surfaces:
				# corte del rayo
				b_r = m*(surface.position - z_o) + r_o
				# Coeficientes del polinomio de orden 4to que se resuelve para obtener
				A4 = surface.T*(m**2 + 1)**2
				A3 = -2*(surface.S - 2*surface.T*b_r*m)*(m**2 + 1)
				A2 = surface.O*(surface.G + m**2 + 1) - 4*surface.S*b_r*m + 2*surface.T*b_r**2*(3*m**2 + 1)
				A1 = 2*(surface.O*b_r*m - surface.S*b_r**2 + 2*surface.T*b_r**3*m - 1)
				A0 = b_r**2*(surface.O + surface.T*b_r**2)
				# se obtienen las raices del polinomio
				# if A4 != 0 and A3 != 0:
				# 	roots = fqs.single_quartic(A4,A3,A2,A1,A0)
				# else:
				# 	roots = fqs.single_quadratic(A2,A1,A0)
				# print(roots)
				roots = surface.solve_quartic(A0,A1,A2,A3,A4)

				line_inter_z = [val.real+surface.position for val in roots if np.isclose([val.imag],[0.0])]
				line_inter = np.array([[val,ray.ray_function(val)] for val in line_inter_z])
				quartic_inter = np.array([surface.surface_function(np.sign(r)*np.sqrt((z-surface.position)**2 + r**2))[0] for z,r in line_inter])
				quartic_inter = np.array([[z+surface.position,r] for z,r in quartic_inter])
				quartic_inter = np.array([qi for li,qi in zip(line_inter,quartic_inter) if np.allclose(qi,li)])
				
				try:
					idxz, = np.nonzero(np.abs(quartic_inter[:,0]-surface.position) == np.min(np.abs(quartic_inter[:,0]-surface.position)))
				except:
					self.rays_paths[i][0].append(0)
					self.rays_paths[i][1].append(0)
					continue
				
				z_inter, r_inter = quartic_inter[idxz][0]
				rho = np.sqrt((z_inter-surface.position)**2 + r_inter**2)
				# para el valor de rho se obtienen el valor del angulo que hace rho con el eje z
				(pz1,pr1),varphi = surface.surface_function(rho)
				if r_inter < 0:
					varphi = -varphi
				# se calcula el vector unitario normal a la superficie
				normal = surface.surface_normal(rho,varphi)
				# se calcula el vector unitario refractado
				refracted = self.refracted_unit_vector(surface.mback.disperssion_formula(ray.wl),surface.mfront.disperssion_formula(ray.wl),incident,normal)
				# se calcula la nueva pendiente del rayo
				m = refracted[1]/refracted[0]
				ray.slope = m
				# nuevo origen del rayo con respecto a la siguiente superficie
				z_o, r_o = (z_inter,r_inter)
				ray.origin = z_o, r_o
				# el vector refractado ahora es el vector incidente de la siguiente superficie
				incident = refracted
				# se agregan las coordenadas del trayecto del rayo a la variable rays_paths
				self.rays_paths[i][0].append(z_inter)
				self.rays_paths[i][1].append(r_inter)
				cost = refracted[0]
			
			self.rays_paths[i][0].append(self.image_position)
			self.rays_paths[i][1].append(ray.ray_function(self.image_position))
			i = i+1

		self.magnification = np.prod([-(s.n_o/s.n_i)*s.z_i/s.z_o for s in self.surfaces])
		
		if self.object_height:
			h = np.linspace(0, self.object_height, 100)
			gt = np.prod([-(s.n_o/s.n_i)*s.z_i/s.z_o for s in self.surfaces])
			self.image_height = gt*h
			self.field_curvature = [s.position + np.sqrt(s.z_i**2 - self.image_height**2) for s in self.surfaces]
		
		#self.field_curvature = np.sum([s.O*(s.n_i-s.n_o)/(s.n_i*s.n_o) for s in self.surfaces])
		#print(1.0/self.field_curvature)

		#self.rays_paths = np.array(self.rays_paths)
		# esto no
		xy = np.unique(np.array(self.rays_paths)[:,:,0],axis=0)

		for zr in xy:
			ids = np.nonzero((np.array(self.rays_paths)[:,:,0] == zr).all(axis=1))[0]
			min, max = np.min(np.array(self.rays_paths)[ids,1,-1]), np.max(np.array(self.rays_paths)[ids,1,-1])
			diff = np.abs(max-min)
			self.distortion.append(diff)
			self.image_tras.append(np.array(self.rays_paths)[ids,1,0][0])

	def edge_thickness(self):
		"""
		La funcion edge_thickness de la clase QuarticOpticalSystem permite calcular el espesor de los extremos de la lente
		a la altura del valor que toma rho_max. Esta funcion no recibe parametros de entrada y retorma el valor del espesor.
		"""
		z_pos = []
		i = 0
		for surface in self.surfaces:
			# solucion de un polinomio de orden 4
			r_o = surface.rho_max
			A4 = surface.S**2+0j
			A3 = -2*surface.S*surface.G*surface.O+0j
			A2 = surface.G*surface.O**2*(surface.G + 1) + 2*surface.S**2*r_o**2+0j
			A1 = -2*surface.G*surface.O*(surface.S*r_o**2 + 1)+0j
			A0 = r_o**2*(surface.G*surface.O**2 + surface.S**2*r_o**2)+0j
			print("{}, {}, {}".format(surface.G,surface.O,surface.S))
			sag_max = np.abs(surface.surface_function(1.1*surface.rho_max+0j)[0][0])
			line_inter = surface.solve_quartic(A0,A1,A2,A3,A4)
			z_inter = [val for val in line_inter if np.abs(val) < sag_max]
			#print(z_inter)
			z_pos.append(z_inter[0])

			rho_max = np.sqrt(z_inter[0]**2 + r_o**2)
			print('rho_0 = {}'.format(rho_max))
			self.surfaces[i].rho_max = rho_max
			i = i+1

		thickness = []
		for i in range(1,len(z_pos)):
			thickness.append(z_pos[i]-z_pos[i-1]+self.surfaces[i].position)

		return thickness

	def view(self,xlim=None,ylim=None):
		"""
		La funcion view de la clase QuarticOpticalSystem permite la visualizacion de todos los elementos del sistema optico y del trazado de rayos.
		"""
		width = 8.5
		height = width / 1.5

		params = {
		'axes.labelsize': 10,
		'legend.fontsize': 10,
		'xtick.labelsize': 10,
		'ytick.labelsize': 10,
		'text.usetex': False,
		'axes.axisbelow': False,
		'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)

		N = 10000
		
		fig, ax = plt.subplots(1,2)

		for en in ax:
			en.spines['right'].set_color('none')
			en.spines['top'].set_color('none')
			en.xaxis.set_ticks_position('bottom')
			en.spines['bottom'].set_position(('data',0))
			en.yaxis.set_ticks_position('left')
			en.spines['left'].set_position(('data',0))

		# plot aperture
		ax[0].plot([self.aperture_position, self.aperture_position], [ self.aperture_size, 1.5*self.aperture_size], lw=4, color='black')
		ax[0].plot([self.aperture_position, self.aperture_position], [-self.aperture_size,-1.5*self.aperture_size], lw=4, color='black')

		# plot medium color
		n_min, n_max = 1.0, 3.0
		for i in range(1,self.surface_number):
			surface1 = self.surfaces[i-1]
			surface2 = self.surfaces[i]
			refractive_index = surface1.n_i
			rho1 = np.linspace(-surface1.rho_max,surface1.rho_max,N)
			rho2 = np.linspace(-surface2.rho_max,surface2.rho_max,N)
			(z1,r1),_ = surface1.surface_function(rho1)
			(z2,r2),_ = surface2.surface_function(rho2)
			z = np.concatenate((z1+surface1.position,z2[::-1]+surface2.position),axis=0)
			r = np.concatenate((r1,r2[::-1]),axis=0)
			ax[0].fill(z, r, 'black', alpha=(refractive_index-n_min)/n_max)

		r = np.linspace(-80,80,10000)
		#zappx = self.surfaces[0].O*(self.surfaces[0].O**2*r**4/4 + r**2)/2 + (-self.surfaces[0].G*self.surfaces[0].O**2 + 2*self.surfaces[0].S)**2*(self.surfaces[0].O**2*r**4/4 + r**2)**2/(8*self.surfaces[0].G*self.surfaces[0].O)
		# -> zappx = (self.surfaces[0].G**2*self.surfaces[0].O**4 - 4*self.surfaces[0].G*self.surfaces[0].S*self.surfaces[0].O**2 + self.surfaces[0].G*self.surfaces[0].O**4 + 4*self.surfaces[0].S**2)/(8*self.surfaces[0].G*self.surfaces[0].O)*r**4 + self.surfaces[0].O/2*r**2
		#ax[0].plot(zappx,r,c='orange')
		# plot surfaces
		for surface in self.surfaces:
			# print("R = {}, K = {}".format(1/surface.O, surface.G))
			rho = np.linspace(-surface.rho_max,surface.rho_max,N)
			(z,r),_ = surface.surface_function(rho)
			ax[0].plot(z+surface.position, r, '-', color='black')

		invf = (self.surfaces[0].n_i-self.surfaces[0].n_o)*(self.surfaces[0].O - self.surfaces[1].O + (self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[0].O*self.surfaces[1].O/self.surfaces[0].n_i)
		focal = 1/invf
		h1 = focal*(self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[1].O/self.surfaces[0].n_i
		h2 = focal*(self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[0].O/self.surfaces[0].n_i
		ax[0].scatter([h1,self.surfaces[1].position-h2],[0,0],s=8)
		print('image position: {}'.format(self.surfaces[1].position - h2 + focal))
		print('focal: {}'.format(focal))
		print('h1 = {}, h2 = {}'.format(h1,h2))
		print('f/#: {}'.format(focal/(2*self.aperture_size)))
		ax[0].scatter(self.z_i,0,s=5)

		# plot ray paths
		for k,ray in enumerate(self.rays_paths):
			zpoints, rpoints = ray
			ax[0].plot(zpoints, rpoints, '-', lw=0.5, c='gray')

		#plot of spot diagram
		if np.array(self.rays_paths).size:
			zpoints, rpoints = np.array(self.rays_paths).T[-1]
			theta = np.linspace(0,2*np.pi, 13)
			for rval in rpoints:
				ax[1].scatter(rval*np.sin(theta),rval*np.cos(theta), s=3, c='black')
		
		ax[0].set_aspect('equal')
		ax[1].set_aspect('equal')

		if xlim is not None:
			ax[0].set_xlim(xlim)
		if ylim is not None:
			ax[0].set_ylim(ylim)

		plt.show()

	def view2(self,xlim=None,ylim=None,zoom_xlim=None,zoom_ylim=None):
		"""
		La funcion view2 de la clase QuarticOpticalSystem permite la visualizacion de todos los elementos del sistema optico y del trazado de rayos.
		"""
		width = 8.5
		height = width / 1.5

		params = {
		'axes.labelsize': 14,
		'legend.fontsize': 14,
		'xtick.labelsize': 14,
		'ytick.labelsize': 14,
		'text.usetex': False,
		'axes.axisbelow': False,
		'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)

		N = 10000
		
		fig, ax = plt.subplots(1,1)

		ax.spines['right'].set_color('none')
		ax.spines['top'].set_color('none')
		ax.xaxis.set_ticks_position('bottom')
		ax.spines['bottom'].set_position(('data',0))
		#ax.yaxis.set_ticks_position('right')
		#ax.spines['left'].set_position(('data',self.image_position))
		ax.yaxis.set_ticks_position('left')
		ax.spines['left'].set_position(('data',0))

		# plot aperture
		ax.plot([self.aperture_position, self.aperture_position], [ self.aperture_size, 1.5*self.aperture_size], lw=4, color='black')
		ax.plot([self.aperture_position, self.aperture_position], [-self.aperture_size,-1.5*self.aperture_size], lw=4, color='black')

		# plot entrance
		if self.entrance_position != None and self.entrance_size != None:
			ax.plot([self.entrance_position, self.entrance_position], [ self.entrance_size, 1.5*self.entrance_size], '--', lw=4, color='blue')
			ax.plot([self.entrance_position, self.entrance_position], [-self.entrance_size,-1.5*self.entrance_size], '--', lw=4, color='blue')

		if self.exit_position != None and self.exit_size != None:
			ax.plot([self.exit_position, self.exit_position], [ self.exit_size, 1.5*self.exit_size], '--', lw=4, color='red')
			ax.plot([self.exit_position, self.exit_position], [-self.exit_size,-1.5*self.exit_size], '--', lw=4, color='red')

		# plot medium color
		n_min, n_max = 1.0, 2.0
		for i in range(1,self.surface_number):
			surface1 = self.surfaces[i-1]
			surface2 = self.surfaces[i]
			refractive_index = surface1.n_i
			rho1 = np.linspace(-surface1.rho_max,surface1.rho_max,N)
			rho2 = np.linspace(-surface2.rho_max,surface2.rho_max,N)
			(z1,r1),_ = surface1.surface_function(rho1)
			(z2,r2),_ = surface2.surface_function(rho2)
			z = np.concatenate((z1+surface1.position,z2[::-1]+surface2.position),axis=0)
			r = np.concatenate((r1,r2[::-1]),axis=0)
			ax.fill(z, r, '#00ff11', alpha=(refractive_index-n_min)/n_max)

		# plot surfaces
		for surface in self.surfaces:
			#print("R = {}, K = {}".format(1/surface.O, surface.G))
			rho = np.linspace(-surface.rho_max,surface.rho_max,N)
			(z,r),_ = surface.surface_function(rho)
			ax.plot(z+surface.position, r, '-', lw=2, alpha=1.0, color='black')

		# invf = (self.surfaces[0].n_i-self.surfaces[0].n_o)*(self.surfaces[0].O - self.surfaces[1].O + (self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[0].O*self.surfaces[1].O/self.surfaces[0].n_i)
		# #focal = 1/invf
		# h1 = focal*(self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[1].O/self.surfaces[0].n_i
		# h2 = focal*(self.surfaces[0].n_i-self.surfaces[0].n_o)*self.surfaces[1].position*self.surfaces[0].O/self.surfaces[0].n_i
		# #ax.scatter([h1,self.surfaces[1].position-h2],[0,0],s=8)
		# print('image position: {}'.format(self.surfaces[1].position - h2 + focal))
		# print('focal: {}'.format(focal))
		# print('h1 = {}, h2 = {}'.format(h1,h2))
		# print('f/#: {}'.format(focal/(2*self.aperture_size)))
		#ax.scatter(self.z_o,0,s=10,c='red')
		#ax.scatter(self.z_i,0,s=10,c='blue')

		# plot ray paths
		for k,ray in enumerate(self.rays_paths):
			zpoints, rpoints = ray
			ax.plot(zpoints[0:-1], rpoints[0:-1], '-', lw=1, c=self.rays[k].color)
			if self.image_position < self.surfaces[-1].position:
				ax.plot(zpoints[-2:], rpoints[-2:], '--', lw=1, c=self.rays[k].color)
			else:
				ax.plot(zpoints[-2:], rpoints[-2:], '-', lw=1, c=self.rays[k].color)

		# i=0
		# for k,ray in enumerate(self.rays_paths):
		# 	zpoints, rpoints = ray
		# 	#print(zpoints)
		# 	d0 = zpoints[0]
		# 	h0 = rpoints[0]
		# 	z0 = zpoints[1]
		# 	r0 = rpoints[1]
		# 	zN = zpoints[-2]
		# 	rN = rpoints[-2]
		# 	hN = self.magnification*h0
		# 	l02 = (z0-d0)**2 + (r0-h0)**2
		# 	dN = zN + abs(rN-hN)*np.sqrt(l02*self.magnification**2/(r0-h0)**2 - 1)
		# 	lN2 = (dN-zN)**2 + (rN-hN)**2
		# 	ax.scatter(zpoints[-1], hN, c='black', s=15)

		# xy = np.array(self.rays_paths).reshape(self.rays_number,-1)[:,[self.surface_number+1,-1]]
		# i = 0
		# initial = 5
		# block_size = 11
		# for x,y in xy[1:-1:11,:]:
		# 	ax.scatter(x,y,c='black')
		#print(np.array(self.rays_paths).reshape(self.rays_number,-1))

		if self.sphere_radius:
			h = self.image_position + self.sphere_radius
			r_s = np.linspace(0,abs(self.object_height),100)
			x_s = h - self.sphere_radius*(1 - (r_s/self.sphere_radius)**2/2 - (r_s/self.sphere_radius)**4/8)#self.sphere_radius*np.sqrt(1 - (r_s/self.sphere_radius)**2)
			ax.plot(x_s, -r_s, '--', c='black')
			ax.plot(x_s,  r_s, '--', c='black')

		#if self.object_height:
		#	ax.plot(self.field_curvature[-1], self.image_height, '--', c='black')
		
		if zoom_xlim is not None and zoom_ylim is not None:
			axins = zoomed_inset_axes(ax, 4, loc=1)

			for k,ray in enumerate(self.rays_paths):
				zpoints, rpoints = ray
				axins.plot(zpoints[-2:], rpoints[-2:], '-', lw=0.5, c=self.rays[k].color)
				#axins.plot(zpoints[-2:], rpoints[-2:], '--', lw=0.5, c=self.rays[k].color)

			#hs = [40.5, 47.8, 50.5]
			#for h in hs:
			#	Rs = self.image_position - h
			#	zs = np.linspace(h, self.image_position, 1000)
			#	rs = np.sqrt(Rs**2 - (zs-h)**2)
			#	axins.plot(zs,rs,c='black',lw=1,zorder=20000)
			#	axins.plot(zs,-rs,c='black',lw=1,zorder=20000)

			# plot surfaces
			# lines = []
			# labels = []
			# i = 0
			# for surface in self.surfaces:
			# 	rho = np.linspace(-surface.rho_max,surface.rho_max,N)
			# 	(z,r),_ = surface.surface_function(rho)
			# 	l, = axins.plot(z+surface.position, r, '-', lw=2, alpha=1.0)
			# 	lines.append(l)
			# 	labels.append('$\Sigma_{}$'.format(i))
			# 	i=i+1

			# axins.legend(lines, labels, loc=0)

			axins.set_xlim(zoom_xlim)
			axins.set_ylim(zoom_ylim)

			axins.set_aspect('equal')

		# ax.set_xlim(-5,188)
		# ax.set_ylim(-110,110)

		ax.set_aspect('equal')

		#ax.xaxis.set_ticks(np.arange(-100, self.image_position+5, 20))

		if xlim is not None:
			ax.set_xlim(xlim)
		if ylim is not None:
			ax.set_ylim(ylim)

		mng = plt.get_current_fig_manager()
		mng.window.showMaximized()

		plt.show()

	def rms_plot(self, points, rays_per_point, h):
		rms_radius = []
		data_screen = np.array(self.rays_paths).reshape((self.rays_number,-1))
		data_idx = [self.surface_number+2-1, 2*(self.surface_number+2)-1]
		
		points_dist = data_screen[:,data_idx].reshape((points, rays_per_point, -1))

		N = rays_per_point
		for rays in points_dist:
			ro = np.sum(rays[:,1])/N
			R = (rays[:,1] - ro)
			Gamma = np.sqrt(np.sum(R**2)/N)
			rms_radius.append(Gamma*1000)

		field = np.linspace(-h, h, points)

		fig, ax = plt.subplots(1,1)

		ax.plot(field, rms_radius)

		ax.set_xlabel('Object distance [$mm$]')
		ax.set_ylabel('RMS spot radius [$\mu m$]')

		plt.show()

	def ray_aberrations(self, rays_number, object_height, aperture_size):
		width = 8.5
		height = width / 3.5

		params = {
		'axes.labelsize': 12,
		'legend.fontsize': 12,
		'xtick.labelsize': 12,
		'ytick.labelsize': 12,
		'text.usetex': False,
		'axes.axisbelow': False,
		'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)

		rp = np.linspace(-aperture_size,aperture_size,rays_number)/aperture_size
		rms_radius = []
		data_screen = np.array(self.rays_paths).reshape((self.rays_number,-1))
		data_idx = [self.surface_number+2-1, 2*(self.surface_number+2)-1]
		points_dist = data_screen[:,data_idx].reshape((rays_number, -1))

		ro = points_dist[:,1][int(rays_number/2)]#np.sum(points_dist[:,1])/rays_number
		R = (points_dist[:,1] - ro)
		
		fig, ax = plt.subplots(1,1)

		ax.spines['right'].set_color('none')
		ax.spines['top'].set_color('none')
		ax.xaxis.set_ticks_position('bottom')
		ax.spines['bottom'].set_position(('data',0))
		#ax.yaxis.set_ticks_position('right')
		#ax.spines['left'].set_position(('data',self.image_position))
		ax.yaxis.set_ticks_position('left')
		ax.spines['left'].set_position(('data',0))

		ax.plot(rp, 1000*(points_dist[:,1]-ro))

		ax.set_xlim([-1,1])
		#ax.set_ylim([-0.1,0.1])

		ax.set_xlabel('Normalized pupil')
		ax.set_ylabel("$e_{y'}[\mu m]$")

		#ax.set_xlabel('Normalized pupil field')
		#ax.set_ylabel('RMS spot radius [$mm$]')

		plt.show()

	def get_rho_values(self):
		"""
		La funcion get_rho_values de la clase QuarticOpticalSystems permite obtener los valores de los parametros
		rho de las superficies.
		"""
		position = np.array([self.surfaces[k].position for k in range(self.surface_number)])
		z = np.array(self.rays_paths).reshape(-1,2*(self.surface_number+2))[:,1:self.surface_number+1]
		r = np.array(self.rays_paths).reshape(-1,2*(self.surface_number+2))[:,self.surface_number+3:-1]
		rho = np.sqrt((z-position)**2 + r**2)
		max_aperture = np.array([np.max(r[:,k]) for k in range(self.surface_number)])

		return rho, max_aperture

	def view_aberrations(self):
		width = 8.5
		height = width / 1.5

		params = {
		'axes.labelsize': 10,
		'legend.fontsize': 10,
		'xtick.labelsize': 10,
		'ytick.labelsize': 10,
		'text.usetex': False,
		'axes.axisbelow': False,
		'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)

		N = 10000
		
		fig, ax = plt.subplots(1,1)

		#ax.spines['right'].set_color('none')
		#ax.spines['top'].set_color('none')
		#ax.xaxis.set_ticks_position('bottom')
		#ax.spines['bottom'].set_position(('data',0))
		#ax.yaxis.set_ticks_position('left')
		#ax.spines['left'].set_position(('data',0))

		# for r_o in np.linspace(-10,10,10):
		# 	z_o = z[0]
		# 	origin = (z_o, r_o)
		# for i in np.linspace(-5,5,10):
		# 	slope = np.tan(i*np.pi/180.0)
		# 	system.add_ray(Ray(slope=slope, origin=origin))

		# system.calculate()
		#ax.plot(self.image_tras, self.distortion,'-', c='black')
		ax.plot(self.distortion,'-', c='black')

		#ax.set_aspect('equal')

		plt.show()