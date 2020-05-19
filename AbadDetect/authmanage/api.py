from authmanage.models import Camera, Profile, TypeUser, DetectedObj
from rest_framework import viewsets, permissions, generics
from .serializers import CameraSerializer, ProfileSerializer, TypeUserSerializer, DetectedObjSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from knox.models import AuthToken

class CameraViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CameraSerializer

    def get_queryset(self):
        return self.request.user.cameras.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProfileSerializer


class TypeUserViewSet(viewsets.ModelViewSet):
    queryset = TypeUser.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TypeUserSerializer
    

class DetectedObjViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = DetectedObjSerializer

    def get_queryset(self):
        return self.request.user.detctedB.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#Register API
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

#Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

#Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user