from django.shortcuts import render
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from apps.home.models import Configuration, Menu, MenuItem, MenuItemElement
from apps.simulation.models import Material

from apps.simulation.gots.system import OpticalSystem

from plotly.offline import plot
import plotly.graph_objs as go

# Create your views here.
class SimulationList(generic.ListView):
	template_name = 'simulation_list.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		try:
			configuration = Configuration.objects.get(pk=1)
		except ObjectDoesNotExist:
			configuration = None

		try:
			menu = Menu.objects.get(pk=1)
			menu_data = {
				'name': menu.name,
				'items': [
					{
						'name': item.name,
						'url': item.url,
						'elements': [
							{'name': element.name, 'url': element.url} for element in MenuItemElement.objects.filter(menu_item=item)
						]
					} for item in MenuItem.objects.filter(menu=menu)
				]
			}
		except ObjectDoesNotExist:
			menu_data = None

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'data': {
				'configuration': configuration,
				'menu': menu_data
			},
			'user': user
		}

		return render(request, self.template_name, response)

class RaytracingSimulation(generic.DetailView):
	template_name = 'raytracing_detail.html'
	materials = Material.objects.all()

	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'user': user,
			'materials': self.materials,
			'simulation': 'false'
		}

		return render(request, self.template_name, response)

	def post(self, request, *args, **kwargs):
		print(request.POST)
		materials = request.POST.getlist('glass')
		first_surf_to_draw = int(request.POST.get('show_from'))
		zeta = [float(val) for val in request.POST.getlist('position')]
		d_obj = [float(val) for val in request.POST.getlist('stg_pts_obj')]
		d_img = [float(val) for val in request.POST.getlist('stg_pts_img')]
		max_apt = [float(val) for val in request.POST.getlist('max_apt')]
		obj_position = float(request.POST.get('obj_position'))
		img_position = float(request.POST.get('img_position'))
		obj_aperture = float(request.POST.get('obj_aperture'))
		img_aperture = float(request.POST.get('img_aperture'))
		stg_obj_obj_plane = float(request.POST.get('stg_obj_obj_plane'))
		stg_img_obj_plane = float(request.POST.get('stg_img_obj_plane'))
		stg_obj_img_plane = float(request.POST.get('stg_obj_img_plane'))
		stg_img_img_plane = float(request.POST.get('stg_img_img_plane'))
		px, py, stop_position = (float(val) for val in request.POST.getlist('aperture_position'))
		stop_radius = float(request.POST.get('aperture_radius'))
		wavelengths = [float(val) for val in request.POST.getlist('wavelengths')]
		fx, fy = (float(val) for val in request.POST.getlist('field_position'))

		# print(request.META)

		# print(materials)
		# print(zeta)
		# print(d_obj)
		# print(d_img)
		# print(max_apt)
		# print(obj_position)
		# print(img_position)
		# print(obj_aperture)
		# print(img_aperture)
		# print(stg_obj_obj_plane)
		# print(stg_img_obj_plane)
		# print(stg_obj_img_plane)
		# print(stg_img_img_plane)
		# print(stop_position)
		# print(stop_radius)
		# print(wavelengths)
		# print(max_field)

		system = OpticalSystem()
		system.set_stop(position=stop_position, central_coordinates=(px, py), radius=stop_radius, point_density=5)

		for i in range(len(wavelengths)):
			if i == 0:
				system.add_spectral_line(wavelength=wavelengths[i], primary=True)
			else:
				system.add_spectral_line(wavelength=wavelengths[i])

		system.set_object_surface(obj_position=obj_position, stigmatic_pair=(stg_obj_obj_plane, stg_img_obj_plane), max_aperture_radius=obj_aperture)

		system.add_source(source_position=(fx, fy))

		for i in range(len(zeta)):
			system.add_surface(
				position=zeta[i],
				stigmatic_pair=(d_obj[i], d_img[i]),
				materials=(materials[i], materials[i+1]),
				max_aperture=max_apt[i],
				idx=i+1
			)

		system.paraxial_parameters()

		system.set_image_surface(img_position=img_position, stigmatic_pair=(stg_obj_img_plane, stg_img_img_plane), max_aperture_radius=img_aperture)

		system.trace_chief_rays()
		system.trace_rays()

		simulation_html = system.show(first_surf_to_draw=first_surf_to_draw)

		if request.user.is_anonymous:
			user = None
		else:
			user = {
				'username': request.user.username,
				'email': request.user.email,
				'is_authenticated': request.user.is_authenticated
			}
		rows = []
		for m, p, s0, s1, ap in zip(materials[1:], zeta, d_obj, d_img, max_apt):
			rows.append(
				{
					'material': m,
					'position': p,
					'stigmatic_obj': s0,
					'stigmatic_img': s1,
					'max_aperture': ap
				}
			)

		response = {
			'success': 'true',
			'message': 'Configuration data fetched successfully',
			'user': user,
			'materials': self.materials,
			'data': {
				'rows': rows,
				'obj_position': obj_position,
				'img_position': img_position,
				'max_apt_obj': obj_aperture,
				'max_apt_img': img_aperture,
				'stg_obj_obj': stg_obj_obj_plane,
				'stg_img_obj': stg_img_obj_plane,
				'stg_obj_img': stg_obj_img_plane,
				'stg_img_img': stg_img_img_plane,
				'obj_glass': materials[0]
			},
			'simulation_html': simulation_html,
			'stop_x': px,
			'stop_y': py,
			'stop_z': stop_position,
			'stop_radius': stop_radius,
			'wavelengths': wavelengths,
			'field_x': fx,
			'field_y': fy,
			'show_from': first_surf_to_draw,
			'simulation': 'true'
		}

		return render(request, self.template_name, response)

