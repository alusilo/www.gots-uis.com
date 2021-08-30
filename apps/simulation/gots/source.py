class Source(object):
	"""docstring for Source"""
	def __init__(self, **kwargs):
		super(Source, self).__init__()
		self.position = kwargs.get('position', None)
		self.color = kwargs.get('color', None)
		self.spectral_lines = []
		self.spectral_lines_number = 0
		self.primary_idx = 0

	def add_spectral_line(self, obj, primary=False):
		self.spectral_lines.append(obj)
		self.spectral_lines_number += 1
		if primary:
			self.primary_idx = self.spectral_lines_number - 1
