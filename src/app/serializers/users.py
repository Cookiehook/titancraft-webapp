from rest_framework import serializers

import app.models.users as models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'is_staff', 'is_superuser']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDetails
        fields = ['id', 'user', 'discord_id', 'avatar_hash']
