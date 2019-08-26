from django.urls import path
from django.conf.urls import url,include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', view.hello),
    #path('save/',view.get_mac),
    #path('search/',view.search),
    #path('getsrcip/',view.getsrcip),
    #path('getdesip/',view.getdesip),
    url('getproto/',views.getprotocol,name='getproto'),
    #path('getip/',view.getip),
    #path('getipinfo',view.getipinfo),
    #path('getfile/',view.getfile)
]