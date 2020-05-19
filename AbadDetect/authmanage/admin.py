from django.contrib import admin
from authmanage.models import TypeUser, Profile, Camera, DetectedObj

admin.site.register(TypeUser)
admin.site.register(Profile)
admin.site.register(Camera)
admin.site.register(DetectedObj)
