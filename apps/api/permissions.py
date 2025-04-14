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

class CanCreateStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.has_perm("staff.add_staff")
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

class CanDeleteSchool(permissions.BasePermission):
    """
    Custom permission to allow only users with delete permission to delete a school.
    """

    def has_permission(self, request, view):
        # Only allow DELETE if the user has delete permissions
        if view.action == "destroy":
            return request.user.has_perm('app_name.delete_school')
        return True