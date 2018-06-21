#from django.contrib import admin
from django.urls import path,include,re_path
from .views import Index
from . import views

urlpatterns = [

    path('',Index,name="index"),
    re_path('api/(?P<q>[\w\-]+)/',views.API.as_view()),
    re_path("gameapi/",views.GameApi.as_view())
]
