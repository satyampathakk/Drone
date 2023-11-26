from django.urls import path
from .views import *
urlpatterns = [
    path('',Monitor.as_view(),name='index'),
    path('user',Creteuser.as_view(),name='user'),
    path('des',Direct.as_view(),name='des'),
    
]
