from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns =[
    path('',views.index, name='index'),
    path('logout/',views.logout, name='logout'),
    path('registry/',views.registry, name='registry'),
    path('taglist/',views.taglist, name='taglist'),
    #url(r'^taglist/(?P<id>\d+)/$', views.taglist, name='taglist'),



]


