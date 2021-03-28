from django.urls import path

from .views import greetingView, covidDataGenerator, createLocation #remember to add this! 

urlpatterns = [
    #path('', greetingView, name='home'),
    path('', covidDataGenerator, name='home'),
    path('<int:pk>/', covidDataGenerator, name='home'),
    path('addcountry/', createLocation, name='newlocation'),
]
