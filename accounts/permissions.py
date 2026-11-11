"""Role based permissions shared by every app."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_role(user):
    """Return 'student', 'recruiter', 'admin' or None for any user object."""
    if not user or not user.is_authenticated:
        return None
    profile = getattr(user, "profile", None)
    if profile is not None:
        return profile.role
    return "admin" if user.is_superuser else None


class IsStudent(BasePermission):
    message = "Student account required"

    def has_permission(self, request, view):
        return get_role(request.user) == "student"


class IsRecruiter(BasePermission):
    message = "Recruiter account required"

    def has_permission(self, request, view):
        return get_role(request.user) == "recruiter"


class IsRecruiterOrReadOnly(BasePermission):
    """Anyone can read. Only recruiters can write."""
    message = "Recruiter login required"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return get_role(request.user) == "recruiter"
