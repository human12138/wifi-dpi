"""wifi_attack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path,re_path
from django.conf.urls import url,include
from . import view
from django.views.generic.base import TemplateView
from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^api/',include('dpi_back.urls')),
    url(r'^$',TemplateView.as_view(template_name="index.html")),
    #path('', view.hello),
    #path('save/',view.get_mac),
    #path('search/',view.search),
    path('gethistory/',view.gethistory),
    #path('getdeip/',view.getdeip),
    #path('getproto/',view.getprotocol,name='getproto'),
    path('getindex/',view.getindex),
    #path('getapinfo',view.getapinfo),
    path('getinfo',view.getinfo),
    path('getfile/',view.getfile),
    path('getflow/',view.getflow)

]
