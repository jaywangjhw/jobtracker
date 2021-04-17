from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', views.companies, name='jobs-companies'),
    path('positions/', views.positions, name='jobs-positions'),
]
