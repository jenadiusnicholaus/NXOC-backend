from rest_framework import serializers

from .models import Membership, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'domain', 'is_active', 'role', 'is_current', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_role(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        membership = obj.memberships.filter(user=request.user).first()
        return membership.role if membership else None

    def get_is_current(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        profile = getattr(request.user, 'profile', None)
        return bool(profile and profile.current_organization_id == obj.id)


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'domain']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context['request']
        organization = Organization.objects.create(**validated_data)
        Membership.objects.create(
            user=request.user,
            organization=organization,
            role=Membership.Role.OWNER,
        )
        profile = request.user.profile
        profile.current_organization = organization
        profile.save(update_fields=['current_organization'])
        return organization
