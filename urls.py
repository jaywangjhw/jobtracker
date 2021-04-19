from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', views.companies, name='jobs-companies'),
    path('companies/new', views.add_company, name='jobs-new-company'),
    path('positions/', views.list_positions, name='jobs-positions'),
    path('positions/new', views.add_position, name='jobs-new-position'),
    path('account/', views.account, name='jobs-account'),
]
