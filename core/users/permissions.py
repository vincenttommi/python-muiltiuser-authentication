from rest_framework.permissions import BasePermission  # Correctly import BasePermission

# Define your custom permissions by inheriting from BasePermission
class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_client)

class IsFreelancerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_freelancer)
