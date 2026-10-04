from django.contrib import admin
from .models import Ticket, TicketComment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'subject', 'status', 'priority', 'organization', 'assignee', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['ticket_id', 'subject', 'requester_name', 'requester_email']


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author_name', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
