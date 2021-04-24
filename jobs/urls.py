from django.urls import path, include
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', views.companies, name='jobs-companies'),
    path('companies/new', views.add_company, name='jobs-new-company'),
    path('positions/', views.list_positions, name='jobs-positions'),
    path('positions/new', views.add_position, name='jobs-new-position'),
    path('positions/<str:pk>/', views.add_position, name='jobs-update-position'),
    path('account/', views.account, name='jobs-account'),
]

#Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
]
