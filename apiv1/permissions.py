from rest_framework import permissions

class IsOwner(permissions.IsAuthenticated):
    """
    Only allow the owner to access things.
    """

    def has_object_permission(self, request, view, obj):
        try:
            return (obj.author == request.user)
        except:
            return (obj == request.user)