from django.contrib.auth import get_user_model
from rest_framework import serializers

try:
    from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer
except ImportError:  # pragma: no cover
    from dj_rest_auth.app_settings import UserDetailsSerializer as DefaultUserDetailsSerializer

from organizations.models import Profile
from organizations.serializers import OrganizationSerializer

User = get_user_model()


class UserDetailsSerializer(DefaultUserDetailsSerializer):
    organizations = serializers.SerializerMethodField()
    current_organization = serializers.SerializerMethodField()

    class Meta(DefaultUserDetailsSerializer.Meta):
        fields = tuple(DefaultUserDetailsSerializer.Meta.fields) + (
            'organizations',
            'current_organization',
        )

    def get_organizations(self, obj):
        memberships = obj.memberships.filter(is_active=True).select_related('organization')
        orgs = [m.organization for m in memberships]
        return OrganizationSerializer(orgs, many=True, context=self.context).data

    def get_current_organization(self, obj):
        profile = getattr(obj, 'profile', None)
        if not profile or not profile.current_organization:
            return None
        return OrganizationSerializer(profile.current_organization, context=self.context).data
