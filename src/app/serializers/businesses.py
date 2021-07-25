from rest_framework import serializers

import app.models.businesses as models


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        fields = ['id', 'name', 'type', 'description', 'x_pos', 'y_pos']


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffMember
        fields = ['id', 'business', 'user']


class StockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StockRecord
        fields = ['id', 'business', 'item', 'cost', 'units', 'last_updated']


class ServiceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceRecord
        fields = ['id', 'business', 'name', 'description']
