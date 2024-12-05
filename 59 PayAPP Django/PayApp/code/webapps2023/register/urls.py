from django.urls import path, include
from . import views

app_name = "register"

urlpatterns = [
    path("", views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('register_admin', views.add_admin, name='register_admin'),
    path('profile', views.view_profile, name="profile")
]