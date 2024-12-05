from django.urls import path
from . import views

app_name = "register"

urlpatterns = [
    path("", views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('camera_stream', views.camera_stream, name="camera_stream"),
    path('end_camera_stream', views.stop_camera_stream, name="end_camera_stream"),
    path('history', views.history, name="history"),
    path('session_history/<str:id>', views.session_history, name="session_history")
]
