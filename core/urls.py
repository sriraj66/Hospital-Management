from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path("profile-p/<int:id>", profile, name="profile"),
    path('login/', login_view, name='login'),
    path("accounts/logout/", logout_view, name='logout'),
    path('register/', register, name='register'),
    path('register/doc', register_doc, name='register_doc'),
]
