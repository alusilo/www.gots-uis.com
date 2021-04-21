from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import render
from rest.app.raytracing.forms import RTForm
from django.forms import formset_factory
from django.http import Http404

from rest_framework import routers, serializers, viewsets, generics
from rest.app.raytracing.serializers import SystemSerializer, MaterialSerializer
from rest.app.raytracing.models import System, Surface, Material
from rest_framework.permissions import AllowAny

from plotly.offline import plot
import plotly.graph_objs as go

from .raytracing.materials import GlassMaterial
from .raytracing.system import QuarticOpticalSystem
from .raytracing.surfaces import QuarticOpticalSurface
from .raytracing.rays import Ray

import numpy as np

materials = {'AIR': 'AIR','N-FK51A': 'N-FK51A','N-FK58': 'N-FK58','N-FK5': 'N-FK5','N-PK51': 'N-PK51','N-PK52A': 'N-PK52A','N-BK10': 'N-BK10','N-BK7': 'N-BK7',
	'N-PSK3': 'N-PSK3','N-PSK53A': 'N-PSK53A','N-ZK7': 'N-ZK7','N-ZK7A': 'N-ZK7A','N-K7': 'N-K7','N-K5': 'N-K5','N-K10': 'N-K10','N-KF9': 'N-KF9','N-BAK2': 'N-BAK2',
	'N-BAK1': 'N-BAK1','N-BAK4': 'N-BAK4','N-BALF5': 'N-BALF5','N-KZFS2': 'N-KZFS2','N-BALF4': 'N-BALF4','N-SK11': 'N-SK11','N-SK5': 'N-SK5','N-SK14': 'N-SK14',
	'N-SK16': 'N-SK16','N-SK4': 'N-SK4','N-SK2': 'N-SK2','N-SSK2': 'N-SSK2','N-SSK5': 'N-SSK5','N-SSK8': 'N-SSK8','N-LAK21': 'N-LAK21','N-LAK7': 'N-LAK7',
	'N-LAK22': 'N-LAK22','N-LAK12': 'N-LAK12','N-LAK14': 'N-LAK14','N-LAK9': 'N-LAK9','N-LAK35': 'N-LAK35','N-LAK34': 'N-LAK34','N-LAK8': 'N-LAK8','N-LAK10': 'N-LAK10',
	'N-LAK33B': 'N-LAK33B','N-F2': 'N-F2','N-SF2': 'N-SF2','N-SF5': 'N-SF5','N-SF8': 'N-SF8','N-SF15': 'N-SF15','N-SF1': 'N-SF1','N-SF10': 'N-SF10','N-SF4': 'N-SF4',
	'N-SF14': 'N-SF14','N-SF11': 'N-SF11','N-SF6': 'N-SF6','N-SF57': 'N-SF57','N-SF66': 'N-SF66','N-BAF10': 'N-BAF10','N-BAF52': 'N-BAF52','N-KZFS4': 'N-KZFS4',
	'N-BAF4': 'N-BAF4','N-BAF51': 'N-BAF51','N-KZFS11': 'N-KZFS11','N-KZFS5': 'N-KZFS5','N-BASF2': 'N-BASF2','N-BASF64': 'N-BASF64','N-KZFS8': 'N-KZFS8','N-LAF7': 'N-LAF7',
	'N-LAF2': 'N-LAF2','N-LAF37': 'N-LAF37','N-LAF35': 'N-LAF35','N-LAF34': 'N-LAF34','N-LAF21': 'N-LAF21','N-LAF33': 'N-LAF33','N-LASF9': 'N-LASF9','N-LASF44': 'N-LASF44',
	'N-LASF43': 'N-LASF43','N-LASF41': 'N-LASF41','N-LASF45': 'N-LASF45','N-LASF31A': 'N-LASF31A','N-LASF40': 'N-LASF40','N-LASF46A': 'N-LASF46A','N-LASF46B': 'N-LASF46B',
	'N-LASF35': 'N-LASF35','CAF2': 'CAF2'}

class MaterialList(generics.ListAPIView):
	queryset = Material.objects.all()
	serializer_class = MaterialSerializer
	permission_classes = [AllowAny]

class SystemList(generics.ListAPIView):
	queryset = System.objects.all()
	serializer_class = SystemSerializer
	permission_classes = [AllowAny]

class SystemDetail(generics.RetrieveAPIView):
	queryset = System.objects.all()
	serializer_class = SystemSerializer
	permission_classes = [AllowAny]

class RayTracingLensView(View):
	template_name = "raytracing.html"

	def get(self, request, pk, *args, **kwargs):
		data = System.objects.get(pk=pk)
		surfaces = Surface.objects.filter(system=pk)
		surfaces_number = len(surfaces)
		system = QuarticOpticalSystem(aperture_position=data.aperture_position, aperture_size=data.aperture_size, image_position=surfaces[surfaces_number-1].img_position, rays_backward=True)

		for obj in surfaces:
			position = obj.position
			materials = [GlassMaterial(material=m) for m in [obj.obj_material, obj.img_material]]
			n_l, n_r = [m.disperssion_formula(data.wavelength) for m in materials]
			d_o, d_i = obj.obj_position, obj.img_position
			if obj.obj_position == 1e24:
				d_o = np.float('inf')
			if obj.img_position == 1e24:
				d_i = np.float('inf')
			parameters = (n_l, n_r, d_o, d_i)
			system.add_surface(QuarticOpticalSurface(parameters=parameters, materials=materials, position=position, rho_max=obj.max_rho))

		entrance_size, entrance_position, exit_size, exit_position = system.system_aperture()
		# end ray-tracing code
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=[data.aperture_position, data.aperture_position], y=[ data.aperture_size, 1.5*data.aperture_size], mode='lines', line=dict(width=4), name='physical aperture', marker_color='black'))
		fig.add_trace(go.Scatter(x=[data.aperture_position, data.aperture_position], y=[-data.aperture_size,-1.5*data.aperture_size], mode='lines', line=dict(width=4), name='physical aperture', marker_color='black'))
		fig.add_trace(go.Scatter(x=[entrance_position, entrance_position], y=[ entrance_size, 1.5*entrance_size], mode='lines', line=dict(width=4), name='entrance pupil', marker_color='blue'))
		fig.add_trace(go.Scatter(x=[entrance_position, entrance_position], y=[-entrance_size,-1.5*entrance_size], mode='lines', line=dict(width=4), name='entrance pupil', marker_color='blue'))
		fig.add_trace(go.Scatter(x=[exit_position, exit_position], y=[ exit_size, 1.5*exit_size], mode='lines', line=dict(width=4), name='exit pupil', marker_color='red'))
		fig.add_trace(go.Scatter(x=[exit_position, exit_position], y=[-exit_size,-1.5*exit_size], mode='lines', line=dict(width=4), name='exit pupil', marker_color='red'))

		i = 0
		N = 200
		for surface in system.surfaces:
			rho = np.linspace(-surface.rho_max,surface.rho_max,N)
			(z,r),_ = surface.surface_function(rho)
			fig.add_trace(go.Scatter(x=z+surface.position, y=r, mode='lines', line=dict(width=2), name='surface'+str(i), marker_color='black'))
			i+=1

		n_min, n_max = 1.0, 2.0
		for i in range(surfaces_number-1):
			surface0 = system.surfaces[i]
			surface1 = system.surfaces[i+1]
			rho0 = np.linspace(-surface0.rho_max,surface0.rho_max,N)
			rho1 = np.linspace(-surface1.rho_max,surface1.rho_max,N)
			(z0,r0),_ = surface0.surface_function(rho0)
			(z1,r1),_ = surface1.surface_function(rho1)
			data_x = np.concatenate((z0+surface0.position,z1[::-1]+surface1.position))
			data_y = np.concatenate((r0,r1[::-1]))
			fig.add_trace(go.Scatter(x=data_x, y=data_y, mode='lines', line=dict(width=0), fill='toself', fillcolor='rgba(0,255,17,{})'.format((surface0.n_i-n_min)/n_max)))

		fig.update_layout(
			title = "Ray-tracing on stigmatic optical system",
			paper_bgcolor='rgba(0,0,0,0)',
    		plot_bgcolor='rgba(0,0,0,0)'
		)
		fig.update_yaxes(
			scaleanchor = "x",
			scaleratio = 1,
		)

		rays_number = 5

		wlg = data.wavelength
		wlb = 0.4861
		wlr = 0.6563
		if surfaces[0].obj_position != 1e24:
			z_o = surfaces[0].obj_position
			for w,c in zip([wlr,wlg,wlb],['red','green','blue']):
				for r_o in [data.object_height,0]:
					origin = (surfaces[0].obj_position, r_o)
					for r in np.linspace(-entrance_size,entrance_size,rays_number):
						op = r-r_o
						ad = (entrance_position-z_o)
						slope = op/ad
						system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))
		else:
			z_o = -10
			for w,c in zip([wlr,wlg,wlb],['red','green','blue']):
				for angle in [0, data.object_height]:
					slope = np.tan(angle)
					for r in np.linspace(-entrance_size,entrance_size,rays_number):
						r_o = r - slope*(entrance_position-z_o)
						origin = (z_o, r_o)
						system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))
		
		try:
			system.calculate()
		except Exception as e:
			print(e)
		else:
			print("Ray paths Ok.")

		i=0
		table1 = ''
		table2 = ''
		for s in system.surfaces:
			G, O, T, S = s.form_parameters()
			table1 += '<tr><td>' + str(i) + '</td><td>' + str(G) + '</td><td>' + str(O) + '</td><td>' + str(T) + '</td><td>' + str(S) + '</td></tr>'
			A4, A6, A8, A10, A12, A14, A16 = s.aspherical_coefficients()
			table2 += '<tr><td>' + str(i) + '</td><td>' + str(A4) + '</td><td>' + str(A6) + '</td><td>' + str(A8) + '</td><td>' + str(A10) + '</td><td>' + str(A12) + '</td><td>' + str(A14) + '</td><td>' + str(A16) + '</td></tr>'
			i=i+1

		# plot ray paths
		i=0
		for k,ray in enumerate(system.rays_paths):
			zpoints, rpoints = ray
			fig.add_trace(go.Scatter(x=zpoints, y=rpoints, mode='lines', line=dict(width=1), name='ray'+str(i), marker_color=system.rays[k].color))
			i+=1

		plot_div = plot(fig, image_width=300, image_height=300, output_type='div', include_plotlyjs=False)

		plot_div = plot_div.replace('\n', '')

		first_idx = plot_div.find('<div>') + 5
		last_idx = plot_div.find('</div>') + 6


		html_container = plot_div[first_idx:last_idx]
		js_content = plot_div[last_idx:-6].replace('<script type="text/javascript">','').replace('</script>','')
		
		return render(request, self.template_name, {'data': {'system_id': pk, 'plot_div': plot_div, 'html_container': html_container, 'js_content': js_content, 'table1': table1, 'table2': table2}})

	def post(self, request, pk, *args, **kwargs):
		aperture_size      = request.POST.get('aperture_size')
		aperture_position  = request.POST.get('aperture_position')
		object_height 	   = request.POST.get('object_height')
		wavelength         = request.POST.get('wavelength')
		surfaces_position  = request.POST.getlist('surfaces_position')
		surfaces_max_rho   = request.POST.getlist('surfaces_max_rho')
		stigmatic_points_o = request.POST.getlist('stigmatic_points_o')
		stigmatic_points_i = request.POST.getlist('stigmatic_points_i')
		materials_o        = request.POST.getlist('materials_o')
		materials_i        = request.POST.getlist('materials_i')
		
		data = System(
			aperture_size=float(aperture_size),
			aperture_position=float(aperture_position),
			object_height=float(object_height),
			wavelength=float(wavelength)
		)
		
		surfaces = [
			Surface(
				system=System.objects.get(pk=pk),
				position=float(sp),
				obj_material=om,
				img_material=im,
				obj_position=float(op),
				img_position=float(ip),
				max_rho=float(mr)
			)
			for sp,om,im,op,ip,mr in zip(surfaces_position,materials_o,materials_i,stigmatic_points_o,stigmatic_points_i,surfaces_max_rho)
		]
		surfaces_number = len(surfaces)
		system = QuarticOpticalSystem(aperture_position=data.aperture_position, aperture_size=data.aperture_size, image_position=surfaces[surfaces_number-1].img_position, rays_backward=True)

		for obj in surfaces:
			position = obj.position
			materials = [GlassMaterial(material=m) for m in [obj.obj_material, obj.img_material]]
			n_l, n_r = [m.disperssion_formula(data.wavelength) for m in materials]
			d_o, d_i = obj.obj_position, obj.img_position
			if obj.obj_position == 1e24:
				d_o = np.float('inf')
			if obj.img_position == 1e24:
				d_i = np.float('inf')
			parameters = (n_l, n_r, d_o, d_i)
			system.add_surface(QuarticOpticalSurface(parameters=parameters, materials=materials, position=position, rho_max=obj.max_rho))

		entrance_size, entrance_position, exit_size, exit_position = system.system_aperture()
		# end ray-tracing code
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=[data.aperture_position, data.aperture_position], y=[ data.aperture_size, 1.5*data.aperture_size], mode='lines', line=dict(width=4), name='physical aperture', marker_color='black'))
		fig.add_trace(go.Scatter(x=[data.aperture_position, data.aperture_position], y=[-data.aperture_size,-1.5*data.aperture_size], mode='lines', line=dict(width=4), name='physical aperture', marker_color='black'))
		fig.add_trace(go.Scatter(x=[entrance_position, entrance_position], y=[ entrance_size, 1.5*entrance_size], mode='lines', line=dict(width=4), name='entrance pupil', marker_color='blue'))
		fig.add_trace(go.Scatter(x=[entrance_position, entrance_position], y=[-entrance_size,-1.5*entrance_size], mode='lines', line=dict(width=4), name='entrance pupil', marker_color='blue'))
		fig.add_trace(go.Scatter(x=[exit_position, exit_position], y=[ exit_size, 1.5*exit_size], mode='lines', line=dict(width=4), name='exit pupil', marker_color='red'))
		fig.add_trace(go.Scatter(x=[exit_position, exit_position], y=[-exit_size,-1.5*exit_size], mode='lines', line=dict(width=4), name='exit pupil', marker_color='red'))

		i = 0
		N = 200
		for surface in system.surfaces:
			rho = np.linspace(-surface.rho_max,surface.rho_max,N)
			(z,r),_ = surface.surface_function(rho)
			fig.add_trace(go.Scatter(x=z+surface.position, y=r, mode='lines', line=dict(width=2), name='surface'+str(i), marker_color='black'))
			i+=1

		fig.update_layout(
			title = "Ray-tracing on stigmatic optical system",
			paper_bgcolor='rgba(0,0,0,0)',
    		plot_bgcolor='rgba(0,0,0,0)'
		)
		fig.update_yaxes(
			scaleanchor = "x",
			scaleratio = 1,
		)

		rays_number = 5

		wlg = data.wavelength
		wlb = 0.4861
		wlr = 0.6563
		if surfaces[0].obj_position != 1e24:
			z_o = surfaces[0].obj_position
			for w,c in zip([wlr,wlg,wlb],['red','green','blue']):
				for r_o in [data.object_height,0]:
					origin = (surfaces[0].obj_position, r_o)
					for r in np.linspace(-entrance_size,entrance_size,rays_number):
						op = r-r_o
						ad = (entrance_position-z_o)
						slope = op/ad
						system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))
		else:
			z_o = -10
			for w,c in zip([wlr,wlg,wlb],['red','green','blue']):
				for angle in [0, data.object_height]:
					slope = np.tan(angle)
					for r in np.linspace(-entrance_size,entrance_size,rays_number):
						r_o = r - slope*(entrance_position-z_o)
						origin = (z_o, r_o)
						system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))
		
		try:
			system.calculate()
		except Exception as e:
			print(e)
		else:
			print("Ray paths Ok.")

		i=0
		table1 = ''
		table2 = ''
		for s in system.surfaces:
			G, O, T, S = s.form_parameters()
			table1 += '<tr><td>' + str(i) + '</td><td>' + str(G) + '</td><td>' + str(O) + '</td><td>' + str(T) + '</td><td>' + str(S) + '</td></tr>'
			A4, A6, A8, A10, A12, A14, A16 = s.aspherical_coefficients()
			table2 += '<tr><td>' + str(i) + '</td><td>' + str(A4) + '</td><td>' + str(A6) + '</td><td>' + str(A8) + '</td><td>' + str(A10) + '</td><td>' + str(A12) + '</td><td>' + str(A14) + '</td><td>' + str(A16) + '</td></tr>'
			i=i+1

		# plot ray paths
		i=0
		for k,ray in enumerate(system.rays_paths):
			zpoints, rpoints = ray
			fig.add_trace(go.Scatter(x=zpoints, y=rpoints, mode='lines', line=dict(width=1), name='ray'+str(i), marker_color=system.rays[k].color))
			i+=1

		plot_div = plot(fig, image_width=300, image_height=300, output_type='div', include_plotlyjs=False)

		plot_div = plot_div.replace('\n', '')

		first_idx = plot_div.find('<div>') + 5
		last_idx = plot_div.find('</div>') + 6


		html_container = plot_div[first_idx:last_idx]
		js_content = plot_div[last_idx:-6].replace('<script type="text/javascript">','').replace('</script>','')
		
		data = {'data': {'system_id': pk, 'html_container': html_container, 'js_content': js_content, 'table1': table1, 'table2': table2}}

		return JsonResponse(data)

		#return render(request, self.template_name, {'data': {'system_id': pk, 'plot_div': plot_div, 'html_container': html_container, 'js_content': js_content, 'table1': table1, 'table2': table2}})

class RayTracingView(View):
	template_name = "dashboard.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'data': ''})

	def post(self, request, *args, **kwargs):
		
		return render(request, self.template_name, {'data': ''})
