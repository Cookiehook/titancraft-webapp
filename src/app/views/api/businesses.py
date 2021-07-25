from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

import app.models.businesses as models
import app.serializers.businesses as serializers


class IsStaffMemberOrReadOnlyPermission(BasePermission):
    """
        Only applied to Business or Business child records.
        User must be a StaffMember for the given business to make edits to any records.
        Must live in this module so it can reference and be referenced by the views that use it
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:  # Flag for admins of entire Webapp
            return True

        # If there is data in the request.POST, check the current user is a staff member
        if request.POST and (isinstance(view, StockRecordViewSet) or isinstance(view, StaffMemberViewSet) or isinstance(view, ServiceRecordViewSet)):
            target_business = models.Business.objects.get(id=request.POST['business'])
            staff = models.StaffMember.objects.filter(business=target_business)
            return request.user in [s.user for s in staff]

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:  # Flag for admins of entire Webapp
            return True

        if isinstance(obj, models.Business):
            staff = models.StaffMember.objects.filter(business=obj)
        elif isinstance(obj, models.StaffMember) or isinstance(obj, models.StockRecord) or isinstance(obj, models.ServiceRecord):
            staff = models.StaffMember.objects.filter(business=obj.business)
        else:
            raise NotImplemented("This permission should only be used for Business related views")

        if len(staff) == 0:  # First time creation of business, add requester as staff
            models.StaffMember(business=obj, user=request.user).save()
            return True
        else:
            return request.user in [s.user for s in staff]


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all().order_by('name')
    serializer_class = serializers.BusinessSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffMemberOrReadOnlyPermission]


class StaffMemberViewSet(viewsets.ModelViewSet):
    queryset = models.StaffMember.objects.all().order_by('user')
    serializer_class = serializers.StaffMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffMemberOrReadOnlyPermission]


class StockRecordViewSet(viewsets.ModelViewSet):
    queryset = models.StockRecord.objects.all().order_by('business')
    serializer_class = serializers.StockRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffMemberOrReadOnlyPermission]


class ServiceRecordViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceRecord.objects.all().order_by('business')
    serializer_class = serializers.ServiceRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffMemberOrReadOnlyPermission]
