from rest_framework.permissions import BasePermission


class IsInAuthorizedGroup(BasePermission):
    def has_permission(self, request, view):
        authorized_group_name = 'Financeiro'
        return request.user.is_authenticated and request.user.groups.filter(name=authorized_group_name).exists()