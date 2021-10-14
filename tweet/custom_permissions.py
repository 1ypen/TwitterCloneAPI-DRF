from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own tweet
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a Tweet instance
        return obj.user == request.user