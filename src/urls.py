from django.urls import path
from src.srcviews import auth_views

urlpatterns = [
    path('register/', auth_views.UserCreate.as_view(), name='account-register'),
    path('login/', auth_views.LoginView.as_view(), name='account-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='account-logout'),
]
