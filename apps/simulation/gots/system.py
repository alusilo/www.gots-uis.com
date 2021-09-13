import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpld3

from apps.simulation.gots.surface import OpticalSurface
from apps.simulation.gots.material import GlassMaterial
from apps.simulation.gots.spectral_line import SpectralLine
from apps.simulation.gots.source import Source
from apps.simulation.gots.stop import CircularStop


class TColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class OpticalSystem(object):
	"""
	Class to create a quartic optical system object

	A quartic optical system object is created using a series of parameters listed below. This object determines the
	environment where the optical components are set. Here is also specified the location of each element with respect
	to the origin of coordinates.
	The valid input parameters are the following:
	* scree_position: position of the screen where the image is registered
	* medium_index: index of refraction of the medium where the optical components are immersed

	There are also parameters determined by the optical components configured by the user. Those auto-defined parameters
	are the following:
	* surfaces_number: Number of optical surfaces in the system
	* rays_number: number of rays to be propagated
	* rays: Array of Rays objects
	* surfaces: Array of Surfaces objects
	* ray_paths: Array of Array of coordinates where each ray meets each surface, including the initial and final
	coordinates.
	* inc_vectors: Array of vectors defining the incident unit vectors for each point on the surface
	* nor_vectors: Array of vectors defining the normal unit vectors for each point on the surface
	* ref_vectors: Array of vectors defining the refracted unit vectors for each point on the surface

	These values allow us to visualize the surfaces composing the system and the rays path through such system.

	To this class belong the add_surface, add_ray, calculate, quartic_intersection, solve_quartic and view functions.

	* add_surface function allow us to add surfaces to the system
	* add_ray function allow us to add rays to the system
	* quartic_intersection function allow us to calculate the intersection values of a ray with a surface
	* solve_quartic function allow us to solve a quartic equation using the Ferrari method
	* calculate function allow us to calculate the rays propagation through the system, to reach the image plane
	* view function allow us to visualize the surfaces and ray trajectories through the system
	"""

	def __init__(self, **kwargs):
		super(OpticalSystem, self).__init__()
		self.obj_position = None
		self.img_position = None
		self.surfaces = []
		self.spectral_lines = []
		self.sources = []
		self.focal_length = None
		self.f_number = None
		self.stop = None
		self.spectral_line = None
		self.stop_grid = None
		self.exit_grid = None
		self.entrance_grid = None
		self.mapMP = None
		self.mapSP = None
		self.CIRCULAR = 0
		self.ANNULAR = 1
		self.RECTANGULAR = 2

	def set_stop(self, aperture = 0, **kwargs):
		position = kwargs.get('position', 0.0)
		central_coordinates = kwargs.get('central_coordinates', (0, 0))
		point_density = kwargs.get('point_density', 0)
		if aperture == self.CIRCULAR:
			radius = kwargs.get('radius', 1.0)
			self.stop = CircularStop(
				position=position,
				central_coordinates=central_coordinates,
				radius=radius,
				point_density=point_density
			)
		elif aperture == self.ANNULAR:
			pass
		elif aperture == self.RECTANGULAR:
			pass
		else:
			print('Error: No aperture type identified!')
			exit(1)

	def add_spectral_line(self, **kwargs):
		fs = kwargs.get('fraunhofer_symbol', None)
		wl = kwargs.get('wavelength', None)
		primary = kwargs.get('primary', False)
		self.spectral_lines.append({'fs': fs, 'wl': wl, 'primary': primary})
		if primary and fs is not None:
			self.spectral_line = SpectralLine(fraunhofer_symbol=fs)
		elif primary and wl is not None:
			self.spectral_line = SpectralLine(wavelength=wl)

	def add_source(self, **kwargs):
		source_position = kwargs.get('source_position', (0.0, 0.0))
		color = kwargs.get('color', None)
		__, __, obj_position = self.surfaces[0].coordinates(source_position)
		source = Source(position=source_position + (obj_position,), color=color)
		for item in self.spectral_lines:
			sline = None
			if item['fs'] is not None:
				sline = SpectralLine(fraunhofer_symbol=item['fs'])
			elif item['wl'] is not None:
				sline = SpectralLine(wavelength=item['wl'])
			source.add_spectral_line(sline, item['primary'])
		self.sources.append(source)

	def set_object_surface(self, **kwargs):
		self.obj_position = kwargs.get('obj_position')
		stigmatic_pair = kwargs.get('stigmatic_pair', (1e24, 1e24))
		object_space_material = kwargs.get('object_space_material', 'AIR')
		max_aperture_radius = kwargs.get('max_aperture_radius', 1.0)
		obj_surface = OpticalSurface(
			position=self.obj_position,
			stigmatic_pair=stigmatic_pair,
			materials=(GlassMaterial(material='REFERENCE'), GlassMaterial(material=object_space_material)),
			wavelength=self.spectral_line.wavelength,
			max_aperture=max_aperture_radius
		)
		self.surfaces.append(obj_surface)

	def set_image_surface(self, **kwargs):
		img_position = kwargs.get('img_position', None)
		auto = kwargs.get('auto', False)
		stigmatic_pair = kwargs.get('stigmatic_pair', (1e24, 1e24))
		image_space_material = kwargs.get('image_space_material', 'AIR')
		max_aperture_radius = kwargs.get('max_aperture_radius', 1.0)
		if auto:
			img_position = self.img_position
		img_surface = OpticalSurface(
			position=img_position,
			stigmatic_pair=stigmatic_pair,
			materials=(GlassMaterial(material=image_space_material), GlassMaterial(material='REFERENCE')),
			wavelength=self.spectral_line.wavelength,
			max_aperture=max_aperture_radius
		)
		self.surfaces.append(img_surface)

	def add_surface(self, **kwargs):
		"""
		The add_surface function receives as input a Surface object, and adds it to the surfaces array.
		"""
		position = kwargs.get('position', 0)
		stigmatic_pair = kwargs.get('stigmatic_pair', (0, 0))
		materials = kwargs.get('materials', ('AIR', 'AIR'))
		max_aperture = kwargs.get('max_aperture', 1.0)
		is_reflective = kwargs.get('is_reflective', False)
		idx = kwargs.get('idx', 1)
		obj = OpticalSurface(
			is_reflective=is_reflective,
			position=position,
			stigmatic_pair=stigmatic_pair,
			materials=(GlassMaterial(material=materials[0]), GlassMaterial(material=materials[1])),
			max_aperture=max_aperture,
			wavelength=self.spectral_line.wavelength
		)
		self.surfaces.insert(idx, obj)

	def paraxial_parameters(self):
		__, __, self.focal_length = self.forward_paraxial_conjugate(
			(0, 0, float('-inf')), self.spectral_line.wavelength)
		__, __, self.img_position = self.forward_paraxial_conjugate(
			(0, 0, self.obj_position), self.spectral_line.wavelength)
		self.exit_grid = []
		self.entrance_grid = []
		self.stop_grid, self.mapMP, self.mapSP = self.stop.grid()
		for coord in self.stop_grid.T:
			self.exit_grid.append(self.forward_paraxial_conjugate(coord, self.spectral_line.wavelength))
			self.entrance_grid.append(self.backward_paraxial_conjugate(coord, self.spectral_line.wavelength))
		self.exit_grid = np.array(self.exit_grid).T
		self.entrance_grid = np.array(self.entrance_grid).T
		# __, self.exit_radius, self.exit_position = self.forward_paraxial_conjugate(
		# 	(0, self.stop.radius, self.stop.position), self.spectral_line.wavelength)
		# __, self.entrance_radius, self.entrance_position = self.backward_paraxial_conjugate(
		# 	(0, self.stop.radius, self.stop.position), self.spectral_line.wavelength)

		# self.f_number = self.focal_length / (2 * self.entrance_radius)
		# self.spectral_line.airy_radius = 1.22 * self.spectral_line.wavelength * self.f_number
		self.spectral_line.airy_radius = 15

		for src in self.sources:
			for sline in src.spectral_lines:
		# 		__, __, focal_length = self.forward_paraxial_conjugate(
		# 			(0, 0, float('-inf')), sline.wavelength)
		# 		__, entrance_radius, __ = self.backward_paraxial_conjugate(
		# 			(0, self.stop.radius, self.stop.position), sline.wavelength)
		# 		f_number = focal_length / (2 * entrance_radius)
		# 		sline.airy_radius = 1.22 * sline.wavelength * f_number
				sline.airy_radius = 15

	def forward_paraxial_conjugate(self, obj_position, wavelength):
		g = 1
		z_img = None
		x_obj, y_obj, z_obj = obj_position
		for s in self.surfaces[1:]:
			n_o = s.obj_space_material.dispersion_formula(wavelength)
			if s.is_reflective:
				n_i = -n_o
			else:
				n_i = s.img_space_material.dispersion_formula(wavelength)
			if s.position > obj_position[2]:
				z_img = s.position + 1 / (s.param_o + (n_o / n_i) * (1 / (z_obj - s.position) - s.param_o))
				g *= np.abs((n_o / n_i) * (z_img - s.position) / (z_obj - s.position))
				z_obj = z_img
		if z_img is None:
			z_img = z_obj

		x_img = g * x_obj
		y_img = g * y_obj

		return x_img, y_img, z_img

	def backward_paraxial_conjugate(self, img_position, wavelength):
		g = 1
		z_obj = None
		x_img, y_img, z_img = img_position
		for s in self.surfaces[1:][::-1]:
			n_o = s.obj_space_material.dispersion_formula(wavelength)
			if s.is_reflective:
				n_i = -n_o
			else:
				n_i = s.img_space_material.dispersion_formula(wavelength)
			if s.position < img_position[2]:
				z_obj = s.position + 1 / (s.param_o + (n_i / n_o) * (1 / (z_img - s.position) - s.param_o))
				g *= np.abs((n_o / n_i) * (z_img - s.position) / (z_obj - s.position))
				z_img = z_obj

		if z_obj is None:
			z_obj = z_img

		x_obj = x_img / g
		y_obj = y_img / g

		return x_obj, y_obj, z_obj

	def aberrations_coefficients(self):
		s_o = self.surfaces[0].position
		defocus_coefficients = []
		spherical_coefficients = []
		grid = self.stop_grid
		d_o = np.max(grid[2])
		for sl in self.spectral_lines:
			s_i = None
			d_i = None
			wl = sl['wl']
			fs = sl['fs']
			line = None
			if wl is not None:
				line = SpectralLine(wavelength=wl)
			elif fs is not None:
				line = SpectralLine(fraunhofer_symbol=fs)
			defocus = 0
			spherical = 0
			g = 1
			rho = None
			for s in self.surfaces[1:-1]:
				n_i = None
				n_o = s.obj_space_material.dispersion_formula(line.wavelength)
				if s.is_reflective:
					n_i = -n_o
				else:
					n_i = s.img_space_material.dispersion_formula(line.wavelength)
				s_i = s.position + 1 / (s.param_o + (n_o / n_i) * (1 / (s_o - s.position) - s.param_o))
				s_o = s_i
				if s.position > np.max(grid[2]):
					d_i = s.position + 1 / (s.param_o + (n_o / n_i) * (1 / (d_o - s.position) - s.param_o))
					g *= np.abs((n_o / n_i) * (d_i - s.position) / (d_o - s.position))
					d_o = d_i
					grid *= g

				xp, yp, zp = grid
				rho_p = np.sqrt(xp ** 2 + yp ** 2)
				rho = rho_p * (s_i - s.position) / (s_i - np.max(zp))
				print(s_i)
				c02 = 0.5 * (n_o * (s.param_o - 1 / (s_o - s.position)) - n_i * (s.param_o - 1 / (s_i - s.position)))
				c04 = 0.125 * ((n_o * (s.param_o - 1 / (s_o - s.position)) ** 2 / (s_o - s.position) - n_i * (s.param_o - 1 / (s_i - s.position)) ** 2 / (s_i - s.position)) + (n_o - n_i) * (2 * s.param_s - s.param_o ** 2 * s.param_g) ** 2 / (s.param_o * s.param_g))
				defocus += c02 * rho ** 2
				spherical += c04 * rho ** 4

			defocus_coefficients.append(spherical)
			spherical_coefficients.append(spherical)

			plt.plot(rho, spherical_coefficients[0])
			plt.show()

	def trace_chief_rays(self):
		entrance_central_coordinates = (
			np.mean(self.entrance_grid[0]),
			np.mean(self.entrance_grid[1]),
			np.max(self.entrance_grid[2])
		)
		for src in self.sources:
			for sline in src.spectral_lines:
				source_position = np.zeros(3)
				source_position[0] = src.position[0]
				source_position[1] = src.position[1]
				source_position[2] = src.position[2]

				incident_vector = (entrance_central_coordinates - source_position) / np.linalg.norm(
					entrance_central_coordinates - source_position
				)
				incident_vector[2] = np.abs(incident_vector[2])

				sline.chief_ray_paths = np.zeros((len(self.surfaces), 3))
				sline.chief_ray_paths[0] = source_position

				k = 1
				for surf in self.surfaces[1:]:
					try:
						intersection = surf.quartic_intersection(source_position, incident_vector)
					except:
						intersection = np.zeros(3)

					sline.chief_ray_paths[k] = intersection

					dx, dy, dz = surf.surface_derivative(intersection)
					nx = dx / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
					ny = dy / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
					nz = dz / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

					normal_vector = np.array([nx, ny, nz])
					if surf.is_reflective:
						t = -1
					else:
						t = surf.obj_space_material.dispersion_formula(
							sline.wavelength) / surf.img_space_material.dispersion_formula(sline.wavelength)
					nu = np.sum(incident_vector * normal_vector, axis=0)
					kn = t * nu + np.sqrt(1 - t ** 2 * (1 - nu ** 2))
					refracted_vector = t * incident_vector - kn * normal_vector

					incident_vector = refracted_vector
					source_position = intersection

					k += 1

	def trace_rays(self, n=0):
		surfaces_number = len(self.surfaces) - 2
		xexp, yexp, zexp = self.entrance_grid
		coords, rays = self.entrance_grid.shape
		vectors_data_shape = (surfaces_number + 1, coords, rays)
		rays_data_shape = (surfaces_number + 2, coords, rays)
		for src in self.sources:
			for sline in src.spectral_lines:
				source_position = np.zeros(self.entrance_grid.shape)
				sline.incident_vector = np.zeros(vectors_data_shape)
				sline.normal_vector = np.zeros(vectors_data_shape)
				sline.refracted_vector = np.zeros(vectors_data_shape)

				source_position[0] = src.position[0]
				source_position[1] = src.position[1]
				source_position[2] = src.position[2]

				ux = (xexp - source_position[0]) / np.sqrt(
					(xexp - source_position[0]) ** 2 + (yexp - source_position[1]) ** 2
					+ (zexp - source_position[2]) ** 2
				)
				uy = (yexp - source_position[1]) / np.sqrt(
					(xexp - source_position[0]) ** 2 + (yexp - source_position[1]) ** 2
					+ (zexp - source_position[2]) ** 2
				)
				uz = np.abs(zexp - source_position[2]) / np.sqrt(
					(xexp - source_position[0]) ** 2 + (yexp - source_position[1]) ** 2
					+ (zexp - source_position[2]) ** 2
				)
				incident_vector = np.array([ux, uy, uz])

				sline.ray_paths = np.zeros(rays_data_shape)
				sline.ray_paths[0] = source_position

				k = 1
				opl = 0
				px, py, pz = None, None, None
				for surf in self.surfaces[1:]:
					sline.incident_vector[k - 1] = incident_vector

					sx, sy, sz = source_position
					ix, iy, iz = incident_vector
					px = np.zeros(rays)
					py = np.zeros(rays)
					pz = np.zeros(rays)
					for i in range(rays):
						sp = np.array([sx[i], sy[i], sz[i]])
						vi = np.array([ix[i], iy[i], iz[i]])
						try:
							px[i], py[i], pz[i] = surf.quartic_intersection(sp, vi)
						except:
							pass

					intersection = np.array([px, py, pz])

					sline.ray_paths[k] = intersection

					dx, dy, dz = surf.surface_derivative(intersection)
					nx = dx / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
					ny = dy / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
					nz = dz / np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
					normal_vector = np.array([nx, ny, nz])
					map_pn = np.nonzero(nz > 0)
					normal_vector[0][map_pn] = -nx[map_pn]
					normal_vector[1][map_pn] = -ny[map_pn]
					normal_vector[2][map_pn] = -nz[map_pn]
					sline.normal_vector[k - 1] = normal_vector

					if surf.is_reflective:
						t = -1
					else:
						t = surf.obj_space_material.dispersion_formula(
							sline.wavelength) / surf.img_space_material.dispersion_formula(sline.wavelength)
					nu = np.sum(incident_vector * normal_vector, axis=0)
					kn = t * nu + np.sqrt(1 - t ** 2 * (1 - nu ** 2))
					refracted_vector = t * incident_vector - kn * normal_vector
					sline.refracted_vector[k - 1] = refracted_vector

					incident_vector = refracted_vector

					source_position = intersection

					k += 1

	def sine_condition(self):
		mcal, kappa = 1.0, 1.0
		src = self.sources[0]
		rms_val = 1.0
		if src.spectral_lines[src.primary_idx].ray_paths is not None:
			for s, data in zip(self.surfaces[1:-1], src.spectral_lines[src.primary_idx].ray_paths[1:-1]):
				nk = s.obj_space_material.dispersion_formula(self.spectral_line.wavelength)
				if s.is_reflective:
					nk1 = -nk
				else:
					nk1 = s.img_space_material.dispersion_formula(self.spectral_line.wavelength)

				x, y, z = data
				rho = np.sqrt(x ** 2 + y ** 2 + (z - s.position) ** 2)
				mcal *= nk1 * (	2 * s.param_s / s.param_g - s.param_o ** 2 - (
						2 * s.param_s / s.param_g - s.param_o / (s.stigmatic_img_position - s.position)
				) * np.sqrt(1.0 + (2 * s.param_s - s.param_g * s.param_o ** 2) * rho ** 2)
						) / (nk * (2 * s.param_s / s.param_g - s.param_o ** 2 - (
						2 * s.param_s / s.param_g - s.param_o / (s.stigmatic_obj_position - s.position)
				) * np.sqrt(1.0 + (2 * s.param_s - s.param_g * s.param_o ** 2) * rho ** 2)))

			rms_val = np.mean(mcal - kappa) ** 2

		return rms_val

	def draw_spot_diagram(self, **kwargs):
		"""
		The draw_spot_diagram function visualize the spot diagram of the system.
		"""
		render = kwargs.get('render', False)
		width = 3
		height = width / 0.75

		params = {
			'axes.labelsize': 12,
			'legend.fontsize': 12,
			'text.color': 'white',
			'xtick.color': 'white',
			'ytick.color': 'white',
			'axes.labelcolor': 'white',
			'legend.facecolor': 'white',
			'axes.edgecolor': 'white',
			'xtick.labelsize': 12,
			'ytick.labelsize': 12,
			'text.usetex': True,
			'axes.axisbelow': False,
			'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)
		plt.style.use('fivethirtyeight')

		fig, axs = plt.subplots(len(self.sources))

		if len(self.sources) == 1:
			axs = [axs]

		for i, src in enumerate(self.sources):
			axs[i].set_facecolor('xkcd:salmon')
			axs[i].set_facecolor((0., 0., 0.))
			for sline in src.spectral_lines:
				if sline.ray_paths is not None:
					x, y, z = sline.ray_paths[-1]
					axs[i].scatter(1000 * x, 1000 * y, s=1, c=sline.color)
				if sline.chief_ray_paths is not None:
					xc, yc, zc = sline.chief_ray_paths.T
					axs[i].scatter([1000 * xc[-1]], [1000 * yc[-1]], s=1, c=sline.color)
					angle = np.linspace(0, 2 * np.pi, 100)
					xp, yp = 1000 * xc[-1] + sline.airy_radius * np.sin(angle), 1000 * yc[-1] + sline.airy_radius * np.cos(
						angle)
					axs[i].plot(xp, yp, '-', lw=1, c=sline.color)

			axs[i].set_xlabel('x (microns)', fontdict={'fontsize': 12, 'fontweight': 'medium'})
			axs[i].set_ylabel('y (microns)', fontdict={'fontsize': 12, 'fontweight': 'medium'})

			axs[i].set_aspect('equal')

			axs[i].set_title('Spot diagram', fontdict={'fontsize': 12, 'fontweight': 'medium'})

		if render:
			plt.show()
		else:
			return mpld3.fig_to_html(fig)

	def draw_ray_aberrations(self, **kwargs):
		"""
		The draw_ray_aberrations function visualize the ray aberrations of the system.
		"""
		render = kwargs.get('render', False)
		width = 8
		height = width / 1.5

		params = {
			'axes.labelsize': 12,
			'legend.fontsize': 12,
			'text.color': 'white',
			'xtick.color': 'white',
			'ytick.color': 'white',
			'axes.labelcolor': 'white',
			'legend.facecolor': 'white',
			'axes.edgecolor': 'white',
			'xtick.labelsize': 12,
			'ytick.labelsize': 12,
			'text.usetex': True,
			'axes.axisbelow': False,
			'figure.figsize': [width, height]
		}
		plt.rcParams.update(params)
		plt.style.use('fivethirtyeight')

		fig, axs = plt.subplots(len(self.sources), 2)
		if len(self.sources) == 1:
			axs = np.array([[axs[0], axs[1]]])

		ex, ey, ez = self.entrance_grid
		rho_x = (ex - np.mean(ex)) / (np.max(ex) - np.mean(ex))
		rho_y = (ey - np.mean(ey)) / (np.max(ey) - np.mean(ey))
		for i, src in enumerate(self.sources):
			for sline in src.spectral_lines:
				if sline.ray_paths is not None:
					x, y, z = sline.ray_paths[-1]
					xc, yc, zc = sline.chief_ray_paths[-1]
					rho_m, a_m = zip(*sorted(zip(list(rho_y[self.mapMP]) + [0], list(y[self.mapMP] - yc) + [0])))
					rho_s, a_s = zip(*sorted(zip(list(rho_x[self.mapSP]) + [0], list(x[self.mapSP] - xc) + [0])))
					axs[i, 0].plot(rho_m, 1000 * np.array(a_m), c=sline.color, lw=1)
					axs[i, 1].plot(rho_s, 1000 * np.array(a_s), c=sline.color, lw=1)
					axs[i, 0].set_facecolor('xkcd:salmon')
					axs[i, 0].set_facecolor((0., 0., 0.))
					axs[i, 1].set_facecolor('xkcd:salmon')
					axs[i, 1].set_facecolor((0., 0., 0.))

			axs[i, 0].set_title('Meridional ray fan', fontdict={'fontsize': 12, 'fontweight': 'medium'})
			axs[i, 0].set_xlabel('Entrance height (normalized)', fontdict={'fontsize': 12, 'fontweight': 'medium'})
			axs[i, 0].set_ylabel(
				'Transverse ray aberration (microns)',
				fontdict={'fontsize': 12, 'fontweight': 'medium'}
			)

			axs[i, 1].set_title('Sagittal ray fan', fontdict={'fontsize': 12, 'fontweight': 'medium'})
			axs[i, 1].set_xlabel('Entrance height (normalized)', fontdict={'fontsize': 12, 'fontweight': 'medium'})
			axs[i, 1].set_ylabel(
				'Transverse ray aberration (microns)',
				fontdict={'fontsize': 12, 'fontweight': 'medium'}
			)

		if render:
			plt.show()
		else:
			return mpld3.fig_to_html(fig, no_extras=True)

	def show(self, **kwargs):
		"""
		The view function visualize the surfaces composing the system and the rays trajectories.
		"""
		render = kwargs.get('render', False)
		show_vectors_on_surface = kwargs.get('show_vectors_on_surface', False)
		fstd = kwargs.get('first_surf_to_draw', 0)
		lstd = kwargs.get('last_surf_to_draw', len(self.surfaces))
		# width = 10.5
		# height = width / 2.3

		# params = {
		# 	'axes.labelsize': 12,
		# 	'legend.fontsize': 12,
		# 	'xtick.labelsize': 12,
		# 	'ytick.labelsize': 12,
		# 	'text.usetex': False,
		# 	'axes.axisbelow': False,
		# 	'figure.figsize': [width, height]
		# }
		# plt.rcParams.update(params)
		# plt.style.use('fivethirtyeight')

		N = 2050
		M = 137

		fig, ax = plt.subplots(1, 1)
		# ax.set_facecolor('xkcd:salmon')
		# ax.set_facecolor((0.6, 0.6, 0.6))

		# chief ray
		for src in self.sources:
			for sline in src.spectral_lines:
				if sline.chief_ray_paths is not None:
					x, y, z = sline.chief_ray_paths.T
					ax.plot(z, y, '-.', c='black', lw=1)

		# marginal and zonal rays
		for src in self.sources:
			for sline in src.spectral_lines:
				if sline.ray_paths is not None:
					for dist in sline.ray_paths.T[self.mapMP]:
						x, y, z = dist
						if src.color is not None:
							ax.plot(z, y, '-', c=src.color, lw=1)
							if z[-1] < self.surfaces[-1].position:
								ax.plot(z[-2:], y[-2:], '--', c=src.color, lw=1)
							else:
								ax.plot(z[-2:], y[-2:], '-', c=src.color, lw=1)
						else:
							ax.plot(z, y, '-', c=sline.color, lw=1)
							if z[-1] < self.surfaces[-1].position:
								ax.plot(z[-2:], y[-2:], '--', c=sline.color, lw=1)
							else:
								ax.plot(z[-2:], y[-2:], '-', c=sline.color, lw=1)

		# unit vectors on the surfaces
		if show_vectors_on_surface:
			for src in self.sources:
				for sline in src.spectral_lines:
					x, y, z, dx, dy, dz = [], [], [], [], [], []
					if sline.ray_paths is not None:
						for ray, vector in zip(sline.ray_paths[1:-1], sline.incident_vector):
							x.append(ray[0][self.mapMP].flatten())
							y.append(ray[1][self.mapMP].flatten())
							z.append(ray[2][self.mapMP].flatten())
							dx.append(vector[0][self.mapMP].flatten())
							dy.append(vector[1][self.mapMP].flatten())
							dz.append(vector[2][self.mapMP].flatten())
						for xp, yp, zp, dxp, dyp, dzp in zip(
								np.array(x).flatten(), np.array(y).flatten(),
								np.array(z).flatten(), np.array(dx).flatten(),
								np.array(dy).flatten(), np.array(dz).flatten()):
							ax.arrow(zp, yp, dzp, dyp, color='blue')

			for src in self.sources:
				for sline in src.spectral_lines:
					x, y, z, dx, dy, dz = [], [], [], [], [], []
					if sline.ray_paths is not None:
						for ray, vector in zip(sline.ray_paths[1:-1], sline.refracted_vector):
							x.append(ray[0][self.mapMP].flatten())
							y.append(ray[1][self.mapMP].flatten())
							z.append(ray[2][self.mapMP].flatten())
							dx.append(vector[0][self.mapMP].flatten())
							dy.append(vector[1][self.mapMP].flatten())
							dz.append(vector[2][self.mapMP].flatten())
						for xp, yp, zp, dxp, dyp, dzp in zip(
								np.array(x).flatten(), np.array(y).flatten(),
								np.array(z).flatten(), np.array(dx).flatten(),
								np.array(dy).flatten(), np.array(dz).flatten()):
							ax.arrow(zp, yp, dzp, dyp, color='green')

			for src in self.sources:
				for sline in src.spectral_lines:
					x, y, z, dx, dy, dz = [], [], [], [], [], []
					if sline.ray_paths is not None:
						for ray, vector in zip(sline.ray_paths[1:-1], sline.normal_vector):
							x.append(ray[0][self.mapMP].flatten())
							y.append(ray[1][self.mapMP].flatten())
							z.append(ray[2][self.mapMP].flatten())
							dx.append(vector[0][self.mapMP].flatten())
							dy.append(vector[1][self.mapMP].flatten())
							dz.append(vector[2][self.mapMP].flatten())
						for xp, yp, zp, dxp, dyp, dzp in zip(
								np.array(x).flatten(), np.array(y).flatten(),
								np.array(z).flatten(), np.array(dx).flatten(),
								np.array(dy).flatten(), np.array(dz).flatten()):
							ax.arrow(zp, yp, dzp, dyp, color='red')

		# object and image points
		ax.scatter([self.surfaces[1].stigmatic_obj_position], [0], c='blue', s=8)
		ax.scatter([self.surfaces[-2].stigmatic_img_position], [0], c='red', s=8)

		y_min_stop, y_max_stop = np.min(self.stop_grid[1]), np.max(self.stop_grid[1])
		y_min_entrance, y_max_entrance = np.min(self.entrance_grid[1]), np.max(self.entrance_grid[1])
		y_min_exit, y_max_exit = np.min(self.exit_grid[1]), np.max(self.exit_grid[1])
		entrance_position = np.max(self.entrance_grid[2])
		exit_position = np.max(self.exit_grid[2])
		# draw stop
		ax.plot(
			[self.stop.position, self.stop.position],
			[y_min_stop, y_min_stop - 0.5 * np.abs(y_max_stop - y_min_stop)],
			lw=4,
			color='black'
		)
		ax.plot(
			[self.stop.position, self.stop.position],
			[y_max_stop, y_max_stop + 0.5 * np.abs(y_max_stop - y_min_stop)],
			color='black'
		)
		# draw entrance pupil
		ax.plot(
			[entrance_position, entrance_position],
			[y_min_entrance, y_min_entrance - 0.5 * np.abs(y_max_entrance - y_min_entrance)],
			'--',
			lw=4,
			color='blue'
		)
		ax.plot(
			[entrance_position, entrance_position],
			[y_max_entrance, y_max_entrance + 0.5 * np.abs(y_max_entrance - y_min_entrance)],
			'--',
			lw=4,
			color='blue'
		)
		# draw exit pupil
		ax.plot(
			[exit_position, exit_position],
			[y_min_exit, y_min_exit - 0.5 * np.abs(y_max_exit - y_min_exit)],
			'--',
			lw=4,
			color='red'
		)
		ax.plot(
			[exit_position, exit_position],
			[y_max_exit, y_max_exit + 0.5 * np.abs(y_max_exit - y_min_exit)],
			'--',
			lw=4,
			color='red'
		)

		# draw surfaces composing the system
		k = 0
		xdata, ydata = [], []
		for surface in self.surfaces:
			rho = np.linspace(0, surface.max_vtx_surf_distance, N)
			theta = np.linspace(0, 2 * np.pi, M)
			mapMP, = np.nonzero((theta == 0) | (theta == np.pi))
			rho, theta = np.meshgrid(rho, theta)
			zeta = surface.surface_function(rho)
			r = np.sqrt(rho ** 2 - zeta ** 2)
			x, y = r * np.sin(theta), r * np.cos(theta)
			z = zeta + surface.position
			if k >= fstd and k <= lstd:
				xdata.append(z[mapMP])
				ydata.append(y[mapMP])
			for val1, val2 in zip(z[mapMP], y[mapMP]):
				ax.plot(val1, val2, '-', c='black', lw=2)
			k += 1

		dx = np.max(xdata) - np.min(xdata)
		dy = np.max(ydata) - np.min(ydata)
		xlimit = (np.min(xdata) - 0.2 * dx, np.max(xdata) + 0.2 * dx)
		ylimit = (np.min(ydata) - 0.2 * dy, np.max(ydata) + 0.2 * dy)

		ax.set_aspect('equal')

		# limits to narrow down the entire system
		ax.set_xlim(xlimit)
		ax.set_ylim(ylimit)

		ax.set_xlabel("axial coord. (z)")
		ax.set_ylabel("transversal coord. (y)")

		# ax.set_title('Optical system')

		# render if it is true
		if render:
			plt.show()
		else:
			return mpld3.fig_to_html(fig)

	def show3d(self, **kwargs):
		"""
		The view function visualize the surfaces composing the system and the rays trajectories.
		"""
		render = kwargs.get('render', False)
		show_vectors_on_surface = kwargs.get('show_vectors_on_surface', False)
		fstd = kwargs.get('first_surf_to_draw', 0)
		lstd = kwargs.get('last_surf_to_draw', len(self.surfaces))
		width = 10.5
		height = width / 2.3

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
		plt.style.use('fivethirtyeight')

		N = 21
		M = 53

		fig = plt.figure()
		ax = Axes3D(fig, box_aspect=None)

		#ax.set_facecolor('xkcd:salmon')
		#ax.set_facecolor((0.6, 0.6, 0.6))

		# draw chief ray
		for src in self.sources:
			for sline in src.spectral_lines:
				if sline.chief_ray_paths is not None:
					x, y, z = sline.chief_ray_paths.T
					ax.plot(z, x, y, '-.', c=sline.color, lw=1)
		# draw marginal and zonal rays
		for src in self.sources:
			for sline in src.spectral_lines:
				if sline.ray_paths is not None:
					for rdist in sline.ray_paths.T:
						for ray in rdist:
							x, y, z = ray
							ax.plot(z[:-1], x[:-1], y[:-1], '-', c=sline.color, lw=1)
							if z[-1] < self.surfaces[-1].position:
								ax.plot(z[-2:], x[-2:], y[-2:], '--', c=sline.color, lw=1)
							else:
								ax.plot(z[-2:], x[-2:], y[-2:], '-', c=sline.color, lw=1)

						for ray in rdist[self.mapSP]:
							x, y, z = ray
							ax.plot(z[:-1], x[:-1], y[:-1], '-', c=sline.color, lw=1)
							if z[-1] < self.surfaces[-1].position:
								ax.plot(z[-2:], x[-2:], y[-2:], '--', c=sline.color, lw=1)
							else:
								ax.plot(z[-2:], x[-2:], y[-2:], '-', c=sline.color, lw=1)

		ax.scatter([self.surfaces[1].stigmatic_obj_position], [0], [0], c='blue', s=8)
		ax.scatter([self.surfaces[-2].stigmatic_img_position], [0], [0], c='red', s=8)

		if self.stop is not None:
			# stop
			r = np.linspace(self.stop.radius, 1.5 * self.stop.radius, 20)
			theta = np.linspace(0, 2 * np.pi, 64)
			r, theta = np.meshgrid(r, theta)
			x, y, z = r * np.cos(theta), r * np.sin(theta), self.stop.position * np.ones(r.shape)
			ax.plot_surface(z, x, y, rstride=1, cstride=1, color='black')

			# entrance
			r = np.linspace(self.entrance_radius, 1.5 * self.entrance_radius, 20)
			theta = np.linspace(0, 2 * np.pi, 64)
			r, theta = np.meshgrid(r, theta)
			x, y, z = r * np.cos(theta), r * np.sin(theta), self.entrance_position * np.ones(r.shape)
			ax.plot_surface(z, x, y, rstride=1, cstride=1, color='blue')

			# exit
			r = np.linspace(self.exit_radius, 1.5 * self.exit_radius, 20)
			theta = np.linspace(0, 2 * np.pi, 64)
			r, theta = np.meshgrid(r, theta)
			x, y, z = r * np.cos(theta), r * np.sin(theta), self.exit_position * np.ones(r.shape)
			ax.plot_surface(z, x, y, rstride=1, cstride=1, color='red')

		# draw surfaces
		xdata, ydata, zdata = [], [], []
		k=0
		for surface in self.surfaces:
			rho = np.linspace(0, surface.max_vtx_surf_distance, N)
			theta = np.linspace(0, 2 * np.pi, M)
			rho, theta = np.meshgrid(rho, theta)
			zeta = surface.surface_function(rho)
			r = np.sqrt(rho ** 2 - zeta ** 2)
			x, y, z = r * np.sin(theta), r * np.cos(theta), zeta + surface.position
			if k >= fstd and k <= lstd:
				xdata.append(z)
				ydata.append(x)
				zdata.append(y)
			ax.plot_wireframe(z, x, y, rstride=13, cstride=10, color='black', linewidth=2)
			# ax.plot_surface(z, x, y, color='white', antialiased=True)
			k+=1

		dx = np.max(xdata) - np.min(xdata)
		dy = np.max(ydata) - np.min(ydata)
		dz = np.max(zdata) - np.min(zdata)

		xlimit = (np.min(xdata) - 0.2 * dx, np.max(xdata) + 0.2 * dx)
		ylimit = (np.min(ydata) - 0.2 * dy, np.max(ydata) + 0.2 * dy)
		zlimit = (np.min(zdata) - 0.2 * dz, np.max(zdata) + 0.2 * dz)

		ax.set_xlim(xlimit)
		ax.set_ylim(ylimit)
		ax.set_zlim(zlimit)

		ax.set_box_aspect((dx, dy, dz))

		ax.set_title('Optical system')
		ax.set_xlabel('z')
		ax.set_ylabel('x')
		ax.set_zlabel('y')

		if render:
			plt.show()

	def print_system_info(self):
		print('############## System information ################')
		print('Stop position: {}'.format(self.stop.position))
		print('Stop radius: {}'.format(self.stop.radius))
		#print('Entrance position: {}'.format(self.entrance_position))
		#print('Entrance radius: {}'.format(self.entrance_radius))
		#print('Exit position: {}'.format(self.exit_position))
		#print('Exit radius: {}'.format(self.exit_radius))
		print('Number of surfaces: {}'.format(len(self.surfaces[1:-1])))
		print('f-number: f/{}'.format(self.f_number))
		print('Focal length: {}'.format(self.focal_length))
		# print('Magnification: {}'.format(self.magnification))
		print(f'{TColors.OKGREEN}Sine condition: {self.sine_condition()}{TColors.ENDC}')
		print('-------------- Surfaces properties -----------------')
		for i, s in enumerate(self.surfaces[1:-1]):
			a4, a6, a8, a10, a12, a14, a16 = s.aspherical_coefficients()
			print('Surface {}:'.format(i))
			print('Position: {}'.format(s.position))
			print('Materials: {} | {}'.format(s.obj_space_material.type, s.img_space_material.type))
			print('Refractive indices: {} | {}'.format(s.obj_space_material.dispersion_formula(self.spectral_line.wavelength), s.img_space_material.dispersion_formula(self.spectral_line.wavelength)))
			print(
				'Shape parameters: G = {} | R = {} | O = {}  | T = {} | S = {}'.format(s.param_g, 1/s.param_o, s.param_o, s.param_t, s.param_s)
			)
			print(
				'Aspherical coefficients: A4 = {} | A6 = {} | A8 = {} | A10 = {} | A12 = {} | A14 = {} | A16 = {}'.format(
					a4, a6, a8, a10, a12, a14, a16
				)
			)
		print('----------------------------------------------------')
		print('Number of sources: {}'.format(len(self.sources)))
		print('+++++++++++++++ Sources properties +++++++++++++++++')
		for i, src in enumerate(self.sources):
			print('Source {}:'.format(i))
			print('position = {}'.format(src.position))
			print('Number of spectral lines: {}'.format(src.spectral_lines_number))
			print('~~~~~~~~~~~~~~~~ Spectral lines properties ~~~~~~~~~~~~~~~~')
			for s in src.spectral_lines:
				print('Fraunhofer symbol: {}'.format(s.fs))
				print('Wavelenght: {}'.format(s.wavelength))
				print('Source: {}'.format(s.source))
				print('Airy radius: {}'.format(s.airy_radius))
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
		print('Sources units are in mm and the rest of units are in microns.')
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
