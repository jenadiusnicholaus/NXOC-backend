from django.conf import settings
from django.db import models
from organizations.models import Organization


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        PENDING = 'pending', 'Pending'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tickets')
    ticket_id = models.CharField(max_length=20, db_index=True, blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    source = models.CharField(max_length=50, blank=True)
    requester_name = models.CharField(max_length=255, blank=True)
    requester_email = models.EmailField(blank=True)
    requester_phone = models.CharField(max_length=50, blank=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    team = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.ticket_id} - {self.subject}'

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            last = Ticket.objects.filter(organization=self.organization).order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.ticket_id = f'TK-{next_id:04d}'
        super().save(*args, **kwargs)


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment on {self.ticket.ticket_id}'
