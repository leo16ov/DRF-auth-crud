from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Project
from .serializers import UserSerializer, ProjectSerializer

# Create your views here.

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        user.save()
        login(request, user)
        return Response({'message': 'Usuario registrado exitosamente'})

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username= username, password= password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user= user)
            return Response({'token': token.key})
        
        else:
            return Response({'error': 'Credenciales invalidas'}, status= 401)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        logout(request)
        return Response({'message': 'Logout exitoso'})
    

class ProjectView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many= True)

        return Response(serializer.data)
    
    def get_queryset(self):
        return Project.objects.filter(user= self.request.user)

    def post(self, request):

        serializer = ProjectSerializer(data= request.data, context= {'request': request})
        print(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    
class ProjectDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk= pk)
        
        if project.user != request.user:
            return Response({'error': 'Peticion no autorizada'}, status= status.HTTP_403_FORBIDDEN)
        
        project.delete()
        return Response({'message': 'Project eliminado exitosamente'}, status= status.HTTP_204_NO_CONTENT)

class ProjectUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    