from django.conf import settings
from django.conf.urls import url
from patch import views

urlpatterns = [
    url(r'index.html', views.welcome),
]

# Initial code here
from patch.controller.backwork import init_web_server
init_web_server()