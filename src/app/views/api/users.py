from rest_framework import viewsets, permissions

import app.models.users as models
import app.serializers.users as serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('username')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = models.UserDetails.objects.all().order_by('user')
    serializer_class = serializers.UserDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
