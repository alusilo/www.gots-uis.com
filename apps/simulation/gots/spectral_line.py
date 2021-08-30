class SpectralLine(object):
	"""docstring for SpectralLine"""
	def __init__(self, **kwargs):
		super(SpectralLine, self).__init__()
		self.fs = kwargs.get('fraunhofer_symbol', None)
		self.wavelength = kwargs.get('wavelength', None)
		if self.wavelength is not None:
			self.color = kwargs.get('color', None)
			if self.color is None:
				self.color = self.wl2color(self.wavelength)
		else:
			self.color = kwargs.get('color', '#000000')
		self.source = kwargs.get('source', 'custom')
		self.ray_paths = None
		self.incident_vector = None
		self.normal_vector = None
		self.refracted_vector = None
		self.chief_ray_paths = None
		self.opl = None
		self.airy_radius = None

		if self.fs == "i":
			self.wavelength = 0.36501
			self.color = "#610061"
			self.source = "Hg"
		if self.fs == "h":
			self.wavelength = 0.40466
			self.color = "#8200c8"
			self.source = "Hg"
		if self.fs == "g":
			self.wavelength = 0.43584
			self.color = "#1d00ff"
			self.source = "Hg"
		if self.fs == "F'":
			self.wavelength = 0.47999
			self.color = "#00d5ff"
			self.source = "Cd"
		if self.fs == 'F':
			self.wavelength = 0.48613
			self.color = "#00efff"
			self.source = "H"
		if self.fs == "e":
			self.wavelength = 0.54607
			self.color = "#96ff00"
			self.source = "Hg"
		if self.fs == "d":
			self.wavelength = 0.58756
			self.color = "#ffe600"
			self.source = "He"
		if self.fs == "D":
			self.wavelength = 0.58930
			self.color = "#ffe200"
			self.source = "Na"
		if self.fs == "C'":
			self.wavelength = 0.64385
			self.color = "#ff0900"
			self.source = "Cd"
		if self.fs == "C":
			self.wavelength = 0.65627
			self.color = "#ff0000"
			self.source = "H"
		if self.fs == "r":
			self.wavelength = 0.70652
			self.color = "#f20000"
			self.source = "He"
		if self.fs == "A'":
			self.wavelength = 0.76820
			self.color = "#7c0000"
			self.source = "K"
		if self.fs == "s":
			self.wavelength = 0.85211
			self.color = "#510000"
			self.source = "Cs"
		if self.fs == "t":
			self.wavelength = 1.01398
			self.color = "#000000"
			self.source = "Hg"

	def wl2color(self, wavelength, gamma=0.8):
		if wavelength >= 0.380 and wavelength <= 0.440:
			attenuation = 0.3 + 0.7 * (wavelength - 0.380) / (0.440 - 0.380)
			R = ((-(wavelength - 0.440) / (0.440 - 0.380)) * attenuation) ** gamma
			G = 0.0
			B = (1.0 * attenuation) ** gamma
		elif wavelength >= 0.440 and wavelength <= 0.490:
			R = 0.0
			G = ((wavelength - 0.440) / (0.490 - 0.440)) ** gamma
			B = 1.0
		elif wavelength >= 0.490 and wavelength <= 0.510:
			R = 0.0
			G = 1.0
			B = (-(wavelength - 0.510) / (0.510 - 0.490)) ** gamma
		elif wavelength >= 0.510 and wavelength <= 0.580:
			R = ((wavelength - 0.510) / (0.580 - 0.510)) ** gamma
			G = 1.0
			B = 0.0
		elif wavelength >= 0.580 and wavelength <= 0.645:
			R = 1.0
			G = (-(wavelength - 0.645) / (0.645 - 0.580)) ** gamma
			B = 0.0
		elif wavelength >= 0.645 and wavelength <= 0.750:
			attenuation = 0.3 + 0.7 * (0.750 - wavelength) / (0.750 - 0.645)
			R = (1.0 * attenuation) ** gamma
			G = 0.0
			B = 0.0
		else:
			R = 0.0
			G = 0.0
			B = 0.0
		return (R, G, B)
