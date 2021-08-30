class ImageSurface(object):
	"""docstring for ImageSurface"""
	def __init__(self, **kwargs):
		super(ImageSurface, self).__init__()
		self.position = kwargs.get('position', 0)
