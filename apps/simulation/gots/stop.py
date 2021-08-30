import numpy as np
import matplotlib.pyplot as plt


class Stop(object):
	"""docstring for Stop"""
	def __init__(self, **kwargs):
		super(Stop, self).__init__()
		self.position = kwargs.get('position', 0)
		self.central_coordinates = kwargs.get('central_coordinates', (0, 0))
		self.point_density = kwargs.get('point_density', 0)


class CircularStop(Stop):
	"""docstring for Stop"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.radius = kwargs.get('radius', 1)

	def grid(self):
		axial_steps = self.point_density + 1
		angular_steps = 4 * (self.point_density + 1)
		angular_sample_size = 2 * np.pi / angular_steps
		t = np.linspace(0, 2 * np.pi - angular_sample_size, angular_steps)
		r = np.linspace(self.radius / axial_steps, self.radius, axial_steps)
		map_meridional_plane, = np.nonzero(np.isclose(t, 0) | np.isclose(t, np.pi))
		map_sagittal_plane, = np.nonzero(np.isclose(t, np.pi / 2.) | np.isclose(t, 3 * np.pi / 2.))
		radial, theta = np.meshgrid(r, t)
		x = self.central_coordinates[0] + radial * np.sin(theta)
		y = self.central_coordinates[1] + radial * np.cos(theta)
		z = self.position * np.ones(radial.shape)

		grid_data = np.array([x.flatten(), y.flatten(), z.flatten()])
		map_meridional_plane, = np.nonzero(np.isclose(grid_data[0], self.central_coordinates[0]))
		map_sagittal_plane, = np.nonzero(np.isclose(grid_data[1], self.central_coordinates[1]))

		return grid_data, map_meridional_plane, map_sagittal_plane


class AnnularStop(Stop):
	"""docstring for Stop"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.min_radius = kwargs.get('min_radius', 0)
		self.max_radius = kwargs.get('max_radius', 1)


class RectangularStop(Stop):
	"""docstring for Stop"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.x_side = kwargs.get('x_side', 1)
		self.y_side = kwargs.get('y_side', 1)


# obj = CircularStop(position=-10, central_coordinate=(2, 3), radius=2, point_density=3)
# (x, y, z), mapMP, mapSP = obj.grid()

# plt.scatter(x, y, color='orange')
# plt.scatter(x[mapMP], y[mapMP], color='blue')
# plt.scatter(x[mapSP], y[mapSP], color='blue')
# plt.show()
