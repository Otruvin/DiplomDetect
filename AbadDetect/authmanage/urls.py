from rest_framework import routers
from . api import ProfileViewSet, CameraViewSet, TypeUserViewSet, DetectedObjViewSet, RegistrationAPI, LoginAPI, UserAPI
from django.urls import path, include
from knox import views as knox_views

router = routers.DefaultRouter()
router.register('api/profiles', ProfileViewSet, 'users')
router.register('api/cameras', CameraViewSet, 'cameras')
router.register('api/types', TypeUserViewSet, 'types')
router.register('api/detected', DetectedObjViewSet, 'detected')

urlpatterns = router.urls
urlpatterns.append(path('api/auth', include('knox.urls')))
urlpatterns.append(path('api/auth/registration', RegistrationAPI.as_view()))
urlpatterns.append(path('api/auth/login', LoginAPI.as_view()))
urlpatterns.append(path('api/auth/user', UserAPI.as_view()))
urlpatterns.append(path('api/auth/logout', knox_views.LoginView.as_view(), name='knox_logout'))