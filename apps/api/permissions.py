from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Allows access only to users in a specific group.
    """

    def has_permission(self, request, view):
        required_group_name = 'staff'  # Change this to your desired group
        return request.user and request.user.groups.filter(name=required_group_name).exists()

class CanDeleteStudent(permissions.BasePermission):
    """
    Custom permission to allow deletion only for users with the 'delete_student' permission.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.has_perm("students.delete_student")
        return True

class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser

class IsInvoiceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Students can only view their own invoices
        return obj.student.user == request.user
