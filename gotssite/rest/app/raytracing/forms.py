from django import forms
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField, JSONField

class RTForm(forms.Form):
	surfaces_number   = forms.IntegerField(min_value=0, max_value=6, initial=0)
	aperture_size     = forms.FloatField(min_value=0.1, max_value=15, initial=5.0)
	aperture_position = forms.FloatField(min_value=-100, max_value=100, initial=0.0)
	wavelength        = forms.FloatField(min_value=0.4, max_value=0.7, initial=0.580)

	def __init__(self, *args, **kwargs):
		super(RTForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
