import numpy as np
from apps.simulation.gots.material import GlassMaterial


class OpticalSurface(object):
    """ Class to create a surface object in 3D

    A surface object needs 4 parameters where one of them are truly 4. The parameters are the following: * position:
    indicates the position of the surface in the optical axis defined as the z axis. * parameters: indicates the four
    parameters that define the Cartesian surface, which are: the refractive index of the medium before the surface (
    n_o), the refractive index of the medium after the surface (n_i), the object position (z_o) and the image
    position (z_i). * refractive_index: this allows the refractive index of the media after the surface independent
    of the surface shape. Setting this parameter differing from n_i allows us to use Cartesian surfaces in different
    kind of media. * max_rho: maximum value of rho. This limits the rays accessing the system and the diameter of the
    surface.

    These parameters are necessary to define the surface function and its derivative.

    To the class belong the surface_function and the surface_derivative functions.

    The surface_function functions receives as input a rho value and returns the r and z coordinates,
    where r includes both x and y coordinates (r^2 = x^2 + y^2). The surface_derivative receives as inputs the
    coordinates x, y and z, and returns the derivative value at that point on the surface.
    """

    def __init__(self, **kwargs):
        super(OpticalSurface, self).__init__()
        self.is_reflective = kwargs.get('is_reflective', False)
        self.position = kwargs.get('position', 0)
        self.stigmatic_obj_position, self.stigmatic_img_position = kwargs.get(
            'stigmatic_pair',
            (self.position, self.position)
        )
        self.obj_space_material, self.img_space_material = kwargs.get(
            'materials',
            (GlassMaterial(material='AIR'), GlassMaterial(material='AIR'))
        )
        self.max_aperture = kwargs.get('max_aperture', 0)
        wavelength = kwargs.get('wavelength', None)

        d_k = self.stigmatic_obj_position - self.position
        d_k1 = self.stigmatic_img_position - self.position
        id_k = 1 / d_k
        id_k1 = 1 / d_k1
        n_k = self.obj_space_material.dispersion_formula(wavelength)
        n_k1 = self.img_space_material.dispersion_formula(wavelength)
        eta_k = -1 if self.is_reflective else n_k / n_k1
        self.param_g = (id_k - id_k1 * eta_k ** 2) ** 2 / (eta_k * (id_k1 - id_k * eta_k) * (id_k - id_k1 * eta_k))
        self.param_t = id_k1 ** 2 * id_k ** 2 * (1 - eta_k) * (1 + eta_k) ** 2 / (
                    4 * eta_k * (id_k - eta_k * id_k1))
        self.param_s = id_k1 * id_k * (1 + eta_k) * (id_k - eta_k ** 2 * id_k1) / (
                    2 * eta_k * (id_k - eta_k * id_k1))
        self.param_o = (id_k1 - eta_k * id_k) / (1 - eta_k)

        self.max_vtx_surf_distance = self.maximum_rho_value()

    def surface_function(self, rho):
        """
        The surface_function receives rho value(s) and returns coordinates values of r and z, where r^2 = x^2 + y^2,
        and rho^2 = r^2 + z^2. The expresion here defined is an explicit parametric exprexion of z as a function of
        rho and r as a function of rho.
        """
        eta = (self.param_o + self.param_t * rho ** 2) * rho ** 2 / (
                1 + self.param_s * rho ** 2 + np.sqrt(
                    1 + (2 * self.param_s - self.param_o ** 2 * self.param_g) * rho ** 2
                )
        )
        return eta

    def surface_derivative(self, intersection):
        """
        The surface_derivative function receives as inputs the coordinates values x, y and z, and returns the
        derivatives values of a implicit expresion of the surfaces. The implicit expresion for the surfaces is a
        quartic equation defined as f(x,y,z) = 0, and its derivatives are defined as df/dx, df/dy and df/dz. These
        values of the derivatives as functions of the coordinates are the key to define the normal vector to the
        surface.
        """
        x, y, z = intersection
        eta = z - self.position
        rho2 = x ** 2 + y ** 2 + eta ** 2
        dfdx = 2 * x * (self.param_o - 2 * self.param_s * eta + 2 * self.param_t * rho2)
        dfdy = 2 * y * (self.param_o - 2 * self.param_s * eta + 2 * self.param_t * rho2)
        dfdz = 2 * eta * (
                self.param_o - 2 * self.param_s * eta + 2 * self.param_t * rho2 + self.param_g * self.param_o
        ) - 2 * self.param_s * rho2 - 2
        return np.array([dfdx, dfdy, dfdz])

    def coordinates(self, source_position):
        x_o, y_o = source_position
        x, y, z = self.quartic_intersection((x_o, y_o, 0), (0, 0, 1))
        return x, y, z

    def maximum_rho_value(self):
        x, y, z = self.quartic_intersection((self.max_aperture, 0, 0), (0, 0, 1))
        return np.sqrt(x ** 2 + y ** 2 + (z - self.position)**2)

    def quartic_intersection(self, src, u):
        """
        The quartic_intersection function receives as input an Ray and a Surface objects, and calculate, using the solve_quartic function, the intersection coordinates of the ray with the surface. These coordinates are the output of this function.
        """
        x_o, y_o, z_o = src
        u_x, u_y, u_z = u
        u_xz, u_yz = u_x / u_z, u_y / u_z
        b_x = u_xz * (self.position - z_o) + x_o
        b_y = u_yz * (self.position - z_o) + y_o
        b2 = b_x ** 2 + b_y ** 2
        bu = b_x * u_xz + b_y * u_yz
        a4 = self.param_t / u_z ** 4 + 0j
        a3 = -2 * (self.param_s - 2 * self.param_t * bu) / u_z ** 2 + 0j
        a2 = self.param_g * self.param_o + self.param_o / u_z ** 2 - 4 * self.param_s * bu \
            + 4 * self.param_t * bu ** 2 + 2 * self.param_t * b2 / u_z ** 2 + 0j
        a1 = 2 * (self.param_o * bu - self.param_s * b2 + 2 * self.param_t * b2 * bu - 1) + 0j
        a0 = b2 * (self.param_o + self.param_t * b2) + 0j

        # roots = self.solve_quartic(a0, a1, a2, a3, a4)
        roots = np.roots((a4, a3, a2, a1, a0))
        roots_real_part = np.array([val.real for val in roots])
        line_inter = np.array([[u_xz * val + b_x, u_yz * val + b_y, val + self.position] for val in roots_real_part])
        quartic_inter = np.array(
            [
                [
                    x,
                    y,
                    self.surface_function(np.sqrt(x ** 2 + y ** 2 + (z - self.position) ** 2)) + self.position
                ] for x, y, z in line_inter]
        )
        quartic_inter = np.array([qi for li, qi in zip(line_inter, quartic_inter) if np.allclose(qi[2], li[2])])
        if len(quartic_inter) == 0:
            result = [x_o, y_o, 0]
        else:
            result = quartic_inter[0]

        for qi in quartic_inter:
            if np.all(np.abs(qi[2] - self.position) < np.abs(result[2] - self.position)):
                result = qi

        return result

    def solve_quartic(self, a0, a1, a2, a3, a4):
        a, b, c, d, e = a4, a3, a2, a1, a0
        z_1, z_2, z_3, z_4 = None, None, None, None
        if np.all(b != 0) and np.all(a != 0):
            p = 0.125 * (8. * a * c - 3. * b ** 2) / a ** 2
            q = 0.125 * (b ** 3 - 4. * a * b * c + 8. * a ** 2 * d) / a ** 3
            D0 = c ** 2 - 3. * b * d + 12. * a * e
            D1 = 2.0 * c ** 3 - 9. * b * c * d + 27. * b ** 2 * e + 27. * a * d ** 2 - 72. * a * c * e
            D = -(D1 ** 2 - 4 * D0 ** 3) / 27.
            if D0 == 0:
                R = D1
            else:
                R = 0.5 * (D1 + np.sqrt(-27. * D))
            Q = complex(R) ** (1 / 3.)
            cuberoots_of_1 = [1, complex(-.5, .75 ** .5), complex(-.5, -.75 ** .5)]
            Qtmp = [Q * cbr1 for cbr1 in cuberoots_of_1]
            Q = Qtmp[0]
            S = 0.5 * np.sqrt(-(2. / 3.) * p + (Q + D0 / Q) / (3. * a))
            if S == 0:
                Q = Qtmp[1]
                S = 0.5 * np.sqrt(-(2. / 3.) * p + (Q + D0 / Q) / (3. * a))
            if S == 0:
                Q = Qtmp[2]
                S = 0.5 * np.sqrt(-(2. / 3.) * p + (Q + D0 / Q) / (3. * a))

            z_1 = -0.25 * b / a - S + 0.5 * np.sqrt(-4. * S ** 2 - 2. * p + q / S)
            z_2 = -0.25 * b / a - S - 0.5 * np.sqrt(-4. * S ** 2 - 2. * p + q / S)
            z_3 = -0.25 * b / a + S + 0.5 * np.sqrt(-4. * S ** 2 - 2. * p - q / S)
            z_4 = -0.25 * b / a + S - 0.5 * np.sqrt(-4. * S ** 2 - 2. * p - q / S)

            return np.array([z_1, z_2, z_3, z_4])
        else:
            z_1 = 0.5 * (-d + np.sqrt(d ** 2 - 4 * c * e)) / c
            z_2 = 0.5 * (-d - np.sqrt(d ** 2 - 4 * c * e)) / c

            return np.array([z_1, z_2])

    def aspherical_coefficients(self):
        a4 = -self.param_s * (self.param_g * self.param_o ** 2 - self.param_s) / (2 * self.param_g * self.param_o)
        a6 = self.param_s * (
                self.param_g * self.param_o ** 2 * (
                        -3 * self.param_g * self.param_o ** 2 - 4 * self.param_o ** 2 + 6 * self.param_s
                ) + 4 * self.param_o ** 2 * self.param_s - 4 * self.param_s ** 2
        ) / (8 * self.param_g * self.param_o)
        a8 = 5 * self.param_s * (
                self.param_g ** 2 * self.param_o ** 2 * (
                        -2 * self.param_g ** 2 * self.param_o ** 4 - 5 * self.param_g * self.param_o ** 4
                        + 6 * self.param_g * self.param_o ** 2 * self.param_s - 3 * self.param_o ** 4
                        + 12 * self.param_o ** 2 * self.param_s - 8 * self.param_s ** 2
                ) + 3 * self.param_g * self.param_o ** 2 * self.param_s * (self.param_o ** 2 - 4 * self.param_s)
                + 4 * self.param_g * self.param_s ** 3 + 4 * self.param_s ** 3
        ) / (32 * self.param_g ** 2 * self.param_o)
        a10 = self.param_s * (
                self.param_g ** 3 * self.param_o ** 4 * (
                        -35 * self.param_g ** 3 * self.param_o ** 6 - 126 * self.param_g ** 2 * self.param_o ** 6
                        + 140 * self.param_g ** 2 * self.param_o ** 4 * self.param_s
                        - 147 * self.param_g * self.param_o ** 6 + 450 * self.param_g * self.param_o ** 4 * self.param_s
                        - 280 * self.param_g * self.param_o ** 2 * self.param_s ** 2 - 56 * self.param_o ** 6
                        + 378 * self.param_o ** 4 * self.param_s - 800 * self.param_o ** 2 * self.param_s ** 2
                        + 280 * self.param_s ** 3
                ) + 4 * self.param_g ** 2 * self.param_o ** 4 * self.param_s * (
                        14 * self.param_o ** 4 - 105 * self.param_o ** 2 * self.param_s + 180 * self.param_s ** 2
                ) - 112 * self.param_g ** 2 * self.param_o ** 2 * self.param_s ** 4
                + 168 * self.param_g * self.param_o ** 4 * self.param_s ** 3
                - 288 * self.param_g * self.param_o ** 2 * self.param_s ** 4 + 32 * self.param_s ** 5
        ) / (128 * self.param_g ** 3 * self.param_o ** 3)
        a12 = 7 * self.param_s * (
                self.param_g ** 3 * self.param_o ** 4 * (
                        -9 * self.param_g ** 4 * self.param_o ** 8 - 42 * self.param_g ** 3 * self.param_o ** 8
                        + 45 * self.param_g ** 3 * self.param_o ** 6 * self.param_s
                        - 72 * self.param_g ** 2 * self.param_o ** 8
                        + 196 * self.param_g ** 2 * self.param_o ** 6 * self.param_s
                        - 120 * self.param_g ** 2 * self.param_o ** 4 * self.param_s ** 2
                        - 54 * self.param_g * self.param_o ** 8 + 280 * self.param_g * self.param_o ** 6 * self.param_s
                        - 490 * self.param_g * self.param_o ** 4 * self.param_s ** 2
                        + 180 * self.param_g * self.param_o ** 2 * self.param_s ** 3 - 15 * self.param_o ** 8
                        + 144 * self.param_o ** 6 * self.param_s - 560 * self.param_o ** 4 * self.param_s ** 2
                        + 700 * self.param_o ** 2 * self.param_s ** 3 - 144 * self.param_s ** 4
                ) + self.param_g ** 2 * self.param_o ** 4 * self.param_s * (
                        15 * self.param_o ** 6 - 168 * self.param_o ** 4 * self.param_s
                        + 600 * self.param_o ** 2 * self.param_s ** 2 - 560 * self.param_s ** 3
                ) + 48 * self.param_g ** 2 * self.param_o ** 2 * self.param_s ** 5
                + 8 * self.param_g * self.param_o ** 4 * self.param_s ** 3 * (9 * self.param_o ** 2 - 40 * self.param_s)
                + 224 * self.param_g * self.param_o ** 2 * self.param_s ** 5
                + 64 * self.param_o ** 2 * self.param_s ** 5 - 32 * self.param_s ** 6
        ) / (256 * self.param_g ** 3 * self.param_o ** 3)
        a14 = 3 * self.param_s * (
                self.param_g ** 4 * self.param_o ** 4 * (
                        -77 * self.param_g ** 5 * self.param_o ** 10 - 440 * self.param_g ** 4 * self.param_o ** 10
                        + 462 * self.param_g ** 4 * self.param_o ** 8 * self.param_s
                        - 990 * self.param_g ** 3 * self.param_o ** 10
                        + 2520 * self.param_g ** 3 * self.param_o ** 8 * self.param_s
                        - 1540 * self.param_g ** 3 * self.param_o ** 6 * self.param_s ** 2
                        - 1100 * self.param_g ** 2 * self.param_o ** 10
                        + 5040 * self.param_g ** 2 * self.param_o ** 8 * self.param_s
                        - 8064 * self.param_g ** 2 * self.param_o ** 6 * self.param_s ** 2
                        + 3080 * self.param_g ** 2 * self.param_o ** 4 * self.param_s ** 3
                        - 605 * self.param_g * self.param_o ** 10
                        + 4500 * self.param_g * self.param_o ** 8 * self.param_s
                        - 14112 * self.param_g * self.param_o ** 6 * self.param_s ** 2
                        + 15680 * self.param_g * self.param_o ** 4 * self.param_s ** 3
                        - 3696 * self.param_g * self.param_o ** 2 * self.param_s ** 4
                        - 132 * self.param_o ** 10 + 1650 * self.param_o ** 8 * self.param_s
                        - 9600 * self.param_o ** 6 * self.param_s ** 2 + 23520 * self.param_o ** 4 * self.param_s ** 3
                        - 18816 * self.param_o ** 2 * self.param_s ** 4 + 2464 * self.param_s ** 5
                ) + 4 * self.param_g ** 3 * self.param_o ** 4 * self.param_s * (
                        33 * self.param_o ** 8 - 495 * self.param_o ** 6 * self.param_s
                        + 2800 * self.param_o ** 4 * self.param_s ** 2 - 5880 * self.param_o ** 2 * self.param_s ** 3
                        + 3360 * self.param_s ** 4) - 704 * self.param_g ** 3 * self.param_o ** 2 * self.param_s ** 6
                + self.param_g ** 2 * self.param_o ** 4 * self.param_s ** 3 * (
                        880 * self.param_o ** 4 - 6720 * self.param_o ** 2 * self.param_s + 13440 * self.param_s ** 2
                ) - 5120 * self.param_g ** 2 * self.param_o ** 2 * self.param_s ** 6
                + 1600 * self.param_g * self.param_o ** 4 * self.param_s ** 5
                - 3840 * self.param_g * self.param_o ** 2 * self.param_s ** 6 + 768 * self.param_g * self.param_s ** 7
                + 384 * self.param_s ** 7
        ) / (1024 * self.param_g ** 4 * self.param_o ** 3)
        a16 = self.param_s * (
                self.param_g ** 5 * self.param_o ** 6 * (
                        - 156156 * self.param_g ** 6 * self.param_o ** 12
                        - 1054053 * self.param_g ** 5 * self.param_o ** 12
                        + 1093092 * self.param_g ** 5 * self.param_o ** 10 * self.param_s
                        - 2927925 * self.param_g ** 4 * self.param_o ** 12
                        + 7135128 * self.param_g ** 4 * self.param_o ** 10 * self.param_s
                        - 4372368 * self.param_g ** 4 * self.param_o ** 8 * self.param_s ** 2
                        - 4294290 * self.param_g ** 3 * self.param_o ** 12
                        + 18242987 * self.param_g ** 3 * self.param_o ** 10 * self.param_s
                        - 27747720 * self.param_g ** 3 * self.param_o ** 8 * self.param_s ** 2
                        + 10930920 * self.param_g ** 3 * self.param_o ** 6 * self.param_s ** 3
                        - 3513510 * self.param_g ** 2 * self.param_o ** 12
                        + 23122148 * self.param_g ** 2 * self.param_o ** 10 * self.param_s
                        - 64862056 * self.param_g ** 2 * self.param_o ** 8 * self.param_s ** 2
                        + 68108040 * self.param_g ** 2 * self.param_o ** 6 * self.param_s ** 3
                        - 17489472 * self.param_g ** 2 * self.param_o ** 4 * self.param_s ** 4
                        - 1522521 * self.param_g * self.param_o ** 12
                        + 14863422 * self.param_g * self.param_o ** 10 * self.param_s
                        - 69360004 * self.param_g * self.param_o ** 8 * self.param_s ** 2
                        + 144458440 * self.param_g * self.param_o ** 6 * self.param_s ** 3
                        - 108972864 * self.param_g * self.param_o ** 4 * self.param_s ** 4
                        + 17489472 * self.param_g * self.param_o ** 2 * self.param_s ** 5
                        - 273273 * self.param_o ** 12 + 4215260 * self.param_o ** 10 * self.param_s
                        - 33022640 * self.param_o ** 8 * self.param_s ** 2
                        + 126088952 * self.param_o ** 6 * self.param_s ** 3
                        - 208005504 * self.param_o ** 4 * self.param_s ** 4
                        + 113008896 * self.param_o ** 2 * self.param_s ** 5 - 9993984 * self.param_s ** 6
                ) + self.param_g ** 4 * self.param_o ** 6 * self.param_s * (
                        273035 * self.param_o ** 10 - 5149340 * self.param_o ** 8 * self.param_s
                        + 40512612 * self.param_o ** 6 * self.param_s ** 2
                        - 141184256 * self.param_o ** 4 * self.param_s ** 3
                        + 192580640 * self.param_o ** 2 * self.param_s ** 4 - 72648576 * self.param_s ** 5
                ) + 2498496 * self.param_g ** 4 * self.param_o ** 4 * self.param_s ** 7
                + self.param_g ** 3 * self.param_o ** 6 * self.param_s ** 3 * (
                        2338532 * self.param_o ** 6 - 25912992 * self.param_o ** 4 * self.param_s
                        + 94086848 * self.param_o ** 2 * self.param_s ** 2 - 110036864 * self.param_s ** 3
                ) + 25945920 * self.param_g ** 3 * self.param_o ** 4 * self.param_s ** 7
                + self.param_g ** 2 * self.param_o ** 6 * self.param_s ** 5 * (
                        6712384 * self.param_o ** 2 - 33582400 * self.param_s
                ) + 35369152 * self.param_g ** 2 * self.param_o ** 4 * self.param_s ** 7
                - 3843840 * self.param_g ** 2 * self.param_o ** 2 * self.param_s ** 8
                + 4792640 * self.param_g * self.param_o ** 4 * self.param_s ** 7
                - 5241600 * self.param_g * self.param_o ** 2 * self.param_s ** 8 + 209664 * self.param_s ** 9) / (
                      745472 * self.param_g ** 5 * self.param_o ** 5
                )

        return a4, a6, a8, a10, a12, a14, a16
