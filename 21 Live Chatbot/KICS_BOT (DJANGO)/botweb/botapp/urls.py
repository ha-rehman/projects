from django.urls import path
from .views import home, question
from django.conf.urls import url

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^question$', question, name='question'),
]
