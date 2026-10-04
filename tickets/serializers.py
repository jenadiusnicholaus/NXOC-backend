from rest_framework import serializers
from .models import Ticket, TicketComment


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'author', 'author_name', 'body', 'is_internal', 'created_at']
        read_only_fields = ['id', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    comments = TicketCommentSerializer(many=True, read_only=True)
    assignee_name = serializers.CharField(source='assignee.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_id', 'subject', 'description', 'status', 'status_display',
            'priority', 'priority_display', 'source', 'requester_name', 'requester_email',
            'requester_phone', 'assignee', 'assignee_name', 'team', 'due_date',
            'comments', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'ticket_id', 'created_at', 'updated_at']
