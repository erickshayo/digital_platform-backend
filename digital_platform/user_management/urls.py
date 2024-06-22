from django.urls import path
from .views import *

app_name = 'user_management'

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginView.as_view()),
    path('user-information', UserInformation.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('update-user', UpdateUserView.as_view()),
    path('nin_info', GetUserInformationByNida.as_view()),
    path('user/<uuid:pk>/change-role/', UserRoleUpdateAPIView.as_view(), name='change_role'),
]