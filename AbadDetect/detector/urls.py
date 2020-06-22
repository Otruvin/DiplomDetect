from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^/(?P<stream_path>(.*?))/$',views.dynamic_stream,name="videostream"),  
    url(r'^stream/$',views.indexscreen),
    url(r'^detectFrame/', views.detectFrame),
    url(r'^getBack/', views.getBack),
    url(r'^createDetectors/', views.createDetectors),
    url(r'^getDetectedImage/', views.getDetectedImage)
   ]