from django.urls import path, include
from .views import *
from . import views
from users import views as user_views


urlpatterns = [
    path('', views.home, name='jobs-home'),
    path('companies/', CompanyListView.as_view(extra_context={'title': 'Companies'}), name='jobs-companies'),
    path('companies/<int:pk>', CompanyDetailView.as_view(), name='jobs-company-detail'),
    path('companies/edit/<int:pk>', CompanyUpdateView.as_view(), name='jobs-company-update'),
    path('companies/new', CompanyCreateView.as_view(extra_context={'title': 'Add Company'}), name='jobs-new-company'),
    path('companies/delete/<int:pk>', CompanyDeleteView.as_view(), name='jobs-company-delete'),
    path('positions/', PositionListView.as_view(), name='jobs-list-positions'),
    path('positions/new', PositionCreateView.as_view(), name='jobs-new-position'),
    path('positions/<int:pk>', PositionUpdateView.as_view(), name='jobs-update-position'),
    path('positions/delete/<int:pk>', PositionDeleteView.as_view(), name='jobs-delete-position'),
    # path('positions/', views.list_positions, name='jobs-positions'),
    # path('positions/new', views.add_position, name='jobs-new-position'),
    # path('positions/<int:pk>/', views.update_position, name='jobs-update-position'),
    # path('positions/delete/<int:pk>/', views.delete_position, name='jobs-delete-position'),
    path('account/', views.account, name='jobs-account'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
]
