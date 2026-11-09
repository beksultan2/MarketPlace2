from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Product'ту өзгөртүү/өчүрүү — анын ээси гана (owner = user.id)."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user.id
