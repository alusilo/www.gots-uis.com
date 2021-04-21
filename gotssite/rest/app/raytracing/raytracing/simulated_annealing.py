import numpy as np
from system import QuarticOpticalSystem
from surfaces import QuarticOpticalSurface
from rays import Ray
from lenses import BqSL
from materials import GlassMaterial

import matplotlib.pyplot as plt
import numpy as np

from random import seed
from random import random

materials = ['N-FK51A', 'N-FK58', 'N-FK5', 'N-PK51', 'N-PK52A', 'N-BK10', 'N-BK7', 'N-PSK3', 'N-PSK53A',
			 'N-ZK7', 'N-ZK7A', 'N-K7', 'N-K5', 'N-K10', 'N-KF9', 'N-BAK2', 'N-BAK1', 'N-BAK4', 'N-BALF5',
			 'N-KZFS2', 'N-BALF4', 'N-SK11', 'N-SK5', 'N-SK14', 'N-SK16', 'N-SK4', 'N-SK2', 'N-SSK2',
			 'N-SSK5', 'N-SSK8', 'N-LAK21', 'N-LAK7', 'N-LAK22', 'N-LAK12', 'N-LAK14', 'N-LAK9', 'N-LAK35',
			 'N-LAK34', 'N-LAK8', 'N-LAK10', 'N-LAK33B', 'N-F2', 'N-SF2', 'N-SF5', 'N-SF8', 'N-SF15', 'N-SF1',
			 'N-SF10', 'N-SF4', 'N-SF14', 'N-SF11', 'N-SF6', 'N-SF57', 'N-SF66', 'N-BAF10', 'N-BAF52',
			 'N-KZFS4', 'N-BAF4', 'N-BAF51', 'N-KZFS11', 'N-KZFS5', 'N-BASF2', 'N-BASF64', 'N-KZFS8', 'N-LAF7',
			 'N-LAF2', 'N-LAF37', 'N-LAF35', 'N-LAF34', 'N-LAF21', 'N-LAF33', 'N-LASF9', 'N-LASF44', 'N-LASF43',
			 'N-LASF41', 'N-LASF45', 'N-LASF31A', 'N-LASF40', 'N-LASF46A', 'N-LASF46B', 'N-LASF35']

def cost_function(snumber,wl,mat,d,zeta,aperture_size,aperture_position,rho_max,rays_number):
	kappa = 1
	Mcal = 1
	n = [m.disperssion_formula(wl) for m in mat]

	G = [(n[k+1]**2/(d[k]-zeta[k]) - n[k]**2/(d[k+1]-zeta[k]))**2/(n[k+1]*n[k]*(n[k+1]/(d[k+1]-zeta[k]) - n[k]/(d[k]-zeta[k]))*(n[k+1]/(d[k]-zeta[k]) - n[k]/(d[k+1]-zeta[k]))) for k in range(snumber)]
	O = [(-n[k]/(d[k] - zeta[k]) + n[k+1]/(d[k+1] - zeta[k]))/(-n[k] + n[k+1]) for k in range(snumber)]
	T = [(-n[k] + n[k+1])*(n[k] + n[k+1])**2/(4*n[k]*n[k+1]*(d[k] - zeta[k])**2*(d[k+1] - zeta[k])**2*(-n[k]/(d[k+1] - zeta[k]) + n[k+1]/(d[k] - zeta[k]))) for k in range(snumber)]
	S = [(n[k] + n[k+1])*(-n[k]**2/(d[k+1] - zeta[k]) + n[k+1]**2/(d[k] - zeta[k]))/(2*n[k]*n[k+1]*(d[k] - zeta[k])*(d[k+1] - zeta[k])*(-n[k]/(d[k+1] - zeta[k]) + n[k+1]/(d[k] - zeta[k]))) for k in range(snumber)]

	system = QuarticOpticalSystem(aperture_position=aperture_position, aperture_size=aperture_size, image_position=d[-1], rays_backward=True)

	for k in range(1,snumber+1):
		parameters = (n[k-1], n[k], d[k-1], d[k])
		materials = (mat[k-1], mat[k])
		system.add_surface(QuarticOpticalSurface(parameters=parameters, materials=materials, position=zeta[k-1], rho_max=rho_max[k-1]))

	# Diverging rays
	# r_o = 0
	# origin = (d[0], r_o)
	# for r in np.linspace(-aperture_size,aperture_size,rays_number):
	# 	op = r-r_o
	# 	ad = np.abs(d[0])
	# 	slope = op/ad
	# 	system.add_ray(Ray(slope=slope, origin=origin, wavelength=wl, color='blue'))

	# parallel rays
	r_o = 0
	z_o = -50
	slope = 0
	for r in np.linspace(r_o-aperture_size,r_o+aperture_size,rays_number):
		origin = (z_o, r)
		system.add_ray(Ray(slope=slope, origin=origin, wavelength=wl, color='blue'))

	try:
		system.calculate()
		rho, max_aperture = system.get_rho_values()

		for k in range(snumber):
			Mcal *= n[k+1]*(2*S[k]/G[k] - O[k]**2 - (2*S[k]/G[k] - O[k]/(d[k+1]-zeta[k]))*np.sqrt(1 + (2*S[k] - G[k]*O[k]**2)*rho[:,k]**2))/(n[k]*(2*S[k]/G[k] - O[k]**2 - (2*S[k]/G[k] - O[k]/(d[k]-zeta[k]))*np.sqrt(1 + (2*S[k] - G[k]*O[k]**2)*rho[:,k]**2)))
		
		rms_val = np.mean(Mcal-kappa)**2
	except:
		rms_val = None

	return rms_val, system

def get_neighbor(d,d_limit,mapD):
	new_d = d
	for k in mapD:
		d_min, d_max = d_limit[k-1]
		value = random()
		new_d[k] = d_min + (value*(d_max - d_min))
	return new_d

def get_neighbor2(zeta,mapZ):
	new_zeta = zeta
	for k in mapZ:
		zeta_min, zeta_max = new_zeta[k-1], new_zeta[k+1]
		value = random()
		new_zeta[k] = zeta_min + (value*(zeta_max - zeta_min))
	return new_zeta

T = 50.0
N = 20
c = 0.98
Tmin = 0.1

snumber = 6
aperture_size = 8
aperture_position = 0
wl = 0.5876
rays_number = 51
points_number = 11
object_position = np.float('-inf')
image_position = 150

# initial
#lm = ['AIR', 'X1', 'AIR', 'X2', 'AIR', 'X3', 'AIR']
#d = [object_position, 200, 180, -300, 230, -300, image_position]
#zeta = [0, 15, 25, 35, 45, 65]

lm = ['AIR', 'N-LASF9', 'AIR', 'N-LAF33', 'AIR', 'N-SF10', 'AIR']

mat = [GlassMaterial(material=m) for m in lm]
d = [object_position, 120, 80, 250.275028950491098, np.float('inf'), 230, image_position]
zeta = [0, 5, 25, 30, 80, 85]
rho_max = [15, 15, 15, 15, 15, 15]
d_limit = [(-500, 500),(-500, 500),(-500, 500),(-500, 500),(-500, 500)]

rms_val,__ = cost_function(snumber,wl,mat,d,zeta,aperture_size,aperture_position,rho_max,rays_number)
print(rms_val)
#seed(1)

states = [d]
costs = [rms_val]

mapD = [1,3,5]
mapZ = []
delta_d = 5
min_rms_val = 1.0e-9
modify_ri = False
if rms_val == None: rms_val = 1.0
while T > Tmin and rms_val > min_rms_val:
	for it in range(N):
		if modify_ri:
			new_mat = [
				GlassMaterial(material='AIR'),
				GlassMaterial(material=np.random.choice(materials)),
				GlassMaterial(material=np.random.choice(materials)),
				GlassMaterial(material=np.random.choice(materials)),
				GlassMaterial(material=np.random.choice(materials))
			]
			# print([m.type for m in new_mat])
		else:
			new_mat = mat
		# modifying surfaces positions
		new_zeta = get_neighbor2(zeta,mapZ)
		# calculate the neighbors parameters
		new_d = get_neighbor(d,d_limit,mapD)
		# calculate de new solution using neighbors
		new_rms_val, system = cost_function(snumber,wl,new_mat,new_d,zeta,aperture_size,aperture_position,rho_max,rays_number)
		# sometimes it returns None for systems not acomplishing the given aperture
		if new_rms_val != None:
			# Calculate de difference in cost of the solutions
			Delta = new_rms_val - rms_val
			# if it is a minimun then it is chosen
			if Delta < 0:
				d = new_d
				rms_val = new_rms_val
				mat = new_mat
				zeta = new_zeta
				states.append(d)
				costs.append(rms_val)
			# Statistical acceptance criteria
			else:
				# generate random number between 0 and 1
				t = np.random.uniform()
				# compare it with an energy magnitude equation
				# if t < np.exp(-Delta/T):
				# 	d = new_d
				# 	rms_val = new_rms_val
				# 	states.append(d)
				# 	mat = new_mat
				#	zeta = new_zeta
				# 	costs.append(rms_val)

		if rms_val <= min_rms_val:# and rms_val > 1e-10:
			system.view2()
			print([m.type for m in mat])
			print([pos for pos in d])
			print(zeta)
			#modify_ri = False
			delta_d = delta_d/2.0
			for k in range(len(d_limit)):
				d_limit[k] = (d[k+1] - delta_d, d[k+1] + delta_d)
			min_rms_val = rms_val/10.
			print('RMS value: {}'.format(rms_val))
			print('New limits: {}'.format(d_limit))

	print('Temperature: {}'.format(T))
	# Linear reduction
	# T = T - c
	# Geometric reduction
	T = c*T
	# Slow-decrease
	# b is an arbitrary constant
	# T = T/(1 + b*T)

n = [m.disperssion_formula(wl) for m in mat]

gt = 1
for k in range(snumber):
	gt *= -(n[k]/n[k+1])*(d[k+1]-zeta[k])/(d[k]-zeta[k])

print('##### Optimal parameters #####')
print('Sine condition fulfillment (RMS value): {}'.format(rms_val))
print('aperture_size = {}'.format(aperture_size))
print('object_position = {}'.format(d[0]))
print('image_position = {}'.format(d[-1]))
print('surfaces_number = {}'.format(snumber))
print('wavelength = {}'.format(wl))
print('surfaces_position = {}'.format(zeta))
print('refractive_indices = {}'.format(n))
print('glass_materials = {}'.format([m.type for m in mat]))
print('stigmatic_points = {}'.format(np.array(d)))
print('transverse_magnification = {}'.format(gt))

aperture_size = 5
system = QuarticOpticalSystem(aperture_position=aperture_position, aperture_size=aperture_size, image_position=d[-1], rays_backward=True)

n = [m.disperssion_formula(wl) for m in mat]

for k in range(1,snumber+1):
	parameters = (n[k-1], n[k], d[k-1], d[k])
	materials = (mat[k-1], mat[k])
	system.add_surface(QuarticOpticalSurface(parameters=parameters, materials=materials, position=zeta[k-1], rho_max=rho_max[k-1]))

rays_number = 3
points_wl = [wl]
color = ['#000000']
for c,w in zip(color,points_wl):
	for r_o in [0]:#np.linspace(-2, 2, points_number):
		origin = (d[0], r_o)
		for r in np.linspace(-aperture_size,aperture_size,rays_number):
			op = r-r_o
			ad = np.abs(d[0])
			slope = op/ad
			system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))

# points_wl = [0.4861, 0.656]
# color = ['#ff0000', '#0000ff']
# for c,w in zip(color,points_wl):
# 	for r_o in [0,0]:
# 		origin = (d[0], r_o)
# 		for r in np.linspace(-aperture_size,aperture_size,rays_number):
# 			op = r-r_o
# 			ad = np.abs(d[0])
# 			slope = op/ad
# 			system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))

# z_o = -50
# points_wl = [wl]
# color = ['#000000']
# for c,w in zip(color,points_wl):
# 	for slope in [-8*np.pi/180, 0]:#np.linspace(-5*np.pi/180, 5*np.pi/180, points_number):
# 		r_o = slope*z_o
# 		for r in np.linspace(r_o-aperture_size,r_o+aperture_size,rays_number):
# 			origin = (z_o, r)
# 			system.add_ray(Ray(slope=slope, origin=origin, wavelength=w, color=c))

system.calculate()

system.view2()

plt.figure()
plt.suptitle("Evolution of states and costs of the simulated annealing")
plt.subplot(121)
for state in np.array(states).T:
	plt.plot(state)
plt.title("States")
plt.subplot(122)
plt.plot(costs, 'b')
plt.title("Costs")
plt.show()