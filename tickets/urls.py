from django.urls import path

from . import views

urlpatterns = [
    path('', views.TicketListCreateView.as_view(), name='ticket-list-create'),
    path('stats/', views.TicketStatsView.as_view(), name='ticket-stats'),
    path('<str:ticket_id>/', views.TicketDetailView.as_view(), name='ticket-detail'),
]
