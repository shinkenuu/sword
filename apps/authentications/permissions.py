from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id == request.user.id


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager


class IsTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_technician
