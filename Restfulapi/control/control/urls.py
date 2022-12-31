"""control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from led import views as viewsled
from quat import views as viewsquat
from led2 import views as viewsled2
from led3 import views as viewsled3
from cua import views as viewcua
urlpatterns = [
    path('admin/', admin.site.urls),
    path('led1/on/', viewsled.turnOn),
    path('led1/off/', viewsled.turnOff),
    path('quat/on/', viewsquat.turnOn),
    path('quat/off/', viewsquat.turnOff),
    path('led2/on/', viewsled2.turnOn),
    path('led2/off/', viewsled2.turnOff),
    path('led3/on/', viewsled3.turnOn),
    path('led3/off/', viewsled3.turnOff),
    path('cua/open/', viewcua.opendoor),
    path('cua/close/', viewcua.closedoor),
]
