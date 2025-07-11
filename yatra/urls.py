from django.contrib import admin
from django.urls import path, include
from .import views

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_list/destination_details/pessanger_detail_def/<str:city_name>',views.pessanger_detail_def,name='pessanger_detail_def'),
    #path('upcoming_trips', views.upcoming_trips, name='upcoming_trips'),
    path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/otp_verification', views.otp_verification, name='otp_verification'),
    path('recommend', views.get_recommendations, name='recommendations'),
    path('initiate/', views.initiate_payment, name='initiate'),
    path('verify/', views.verify_payment, name='verify_payment'),
]
