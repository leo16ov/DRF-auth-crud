from django.urls import path
from .views import UserRegisterView ,UserLoginView, UserLogoutView, ProjectView, ProjectDeleteView, ProjectUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name= 'register'),
    path('login/', UserLoginView.as_view(), name= 'login'),
    path('logout/', UserLogoutView.as_view(), name= 'logout'),
    path('project/', ProjectView.as_view(), name= 'project'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name= 'project-delete'),
    path('project/<int:pk>/', ProjectUpdateView.as_view(), name= 'project-update')
]