from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('current/', views.CurrentOrganizationView.as_view(), name='organization-current'),
    path('<int:pk>/select/', views.SelectOrganizationView.as_view(), name='organization-select'),
]
