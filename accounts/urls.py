from django.urls import path
from . import views 

urlpatterns = [
    path('signin', views.RegisterUserView.as_view(), name='sign_user'),
    path('login', views.LoginUserView.as_view(), name='login_user'),
    path('manage', views.ManageUserAccountView.as_view(), name='manage_user')
]