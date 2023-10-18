from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home),
    # path('connect/',views.home,name='board-connect'),
]