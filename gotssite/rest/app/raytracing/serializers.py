from rest_framework import serializers
from rest.app.raytracing.models import System, Surface, Material

class SurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surface
        fields = ('position', 'obj_material', 'img_material', 'obj_position', 'img_position', 'max_rho')

class SystemSerializer(serializers.ModelSerializer):
    surfaces = SurfaceSerializer(many=True)
    class Meta:
        model = System
        fields = ('pk', 'aperture_size', 'aperture_position', 'wavelength', 'object_height', 'surfaces')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('pk', 'name')