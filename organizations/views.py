from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization
from .serializers import OrganizationCreateSerializer, OrganizationSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user, memberships__is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrganizationCreateSerializer
        return OrganizationSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        output = OrganizationSerializer(organization, context={'request': request})
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


class CurrentOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        if not profile.current_organization:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        serializer = OrganizationSerializer(profile.current_organization, context={'request': request})
        return Response(serializer.data)


class SelectOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        organization = get_object_or_404(
            Organization,
            pk=pk,
            memberships__user=request.user,
            memberships__is_active=True,
        )
        profile = request.user.profile
        profile.current_organization = organization
        profile.save(update_fields=['current_organization'])
        serializer = OrganizationSerializer(organization, context={'request': request})
        return Response(serializer.data)
