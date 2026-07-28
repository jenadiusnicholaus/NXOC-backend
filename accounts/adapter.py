from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    def get_reset_password_from_key_url(self, key: str) -> str:
        frontend_url = getattr(settings, 'FRONTEND_URL', '').rstrip('/')
        return f'{frontend_url}/auth/reset-password/confirm/{key}/'

    def get_email_confirmation_url(self, request, emailconfirmation) -> str:
        frontend_url = getattr(settings, 'FRONTEND_URL', '').rstrip('/')
        return f'{frontend_url}/auth/verify-email/{emailconfirmation.key}/'
