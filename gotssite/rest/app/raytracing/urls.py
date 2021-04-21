from django.conf.urls import url
from rest.app.raytracing.views import RayTracingView, RayTracingLensView, SystemList, SystemDetail, MaterialList
from rest_framework import routers

app_name = 'raytracing'

urlpatterns = [
    url(r'raytracing/$', RayTracingView.as_view(), name='index'),
    url(r'raytracing/singlet/(?P<pk>[0-9]+)/$', RayTracingLensView.as_view(), name='lens'),
    url(r'raytracing/materials_list', MaterialList.as_view(), name='materials_list'),
    url(r'raytracing/systems_list', SystemList.as_view(), name='systems_list'),
    url(r'raytracing/system_detail/(?P<pk>[0-9]+)/$', SystemDetail.as_view(), name='system_detail'),
]