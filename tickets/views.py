from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket
from .serializers import TicketSerializer


class TicketListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        profile = getattr(self.request.user, 'profile', None)
        org = profile.current_organization if profile else None
        queryset = Ticket.objects.filter(organization=org) if org else Ticket.objects.none()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        priority_param = self.request.query_params.get('priority')
        if priority_param:
            queryset = queryset.filter(priority=priority_param)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(subject__icontains=search) |
                Q(ticket_id__icontains=search) |
                Q(requester_name__icontains=search)
            )
        return queryset.select_related('assignee').prefetch_related('comments')

    def perform_create(self, serializer):
        profile = getattr(self.request.user, 'profile', None)
        org = profile.current_organization if profile else None
        serializer.save(organization=org)


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    lookup_field = 'ticket_id'

    def get_queryset(self):
        profile = getattr(self.request.user, 'profile', None)
        org = profile.current_organization if profile else None
        return Ticket.objects.filter(organization=org)


class TicketStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        org = profile.current_organization if profile else None
        queryset = Ticket.objects.filter(organization=org) if org else Ticket.objects.none()
        all_count = queryset.count()
        stats = {
            'open': queryset.filter(status='open').count(),
            'in_progress': queryset.filter(status='in_progress').count(),
            'pending': queryset.filter(status='pending').count(),
            'resolved': queryset.filter(status='resolved').count(),
            'closed': queryset.filter(status='closed').count(),
            'all': all_count,
        }
        return Response(stats)
