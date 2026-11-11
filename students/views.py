from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsStudent
from .models import StudentProfile
from .serializers import StudentProfileSerializer


def _ser(r, obj=None, partial=False):
    return StudentProfileSerializer(obj, data=r.data, partial=partial, context={"request": r})


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsStudent])
def profile(r):
    """GET own profile. PUT/PATCH update it (creates it if it does not exist yet)."""
    obj = StudentProfile.objects.filter(user=r.user).first()

    if r.method == "GET":
        if not obj:
            return Response({"detail": "Profile not created yet."}, status=404)
        return Response(StudentProfileSerializer(obj, context={"request": r}).data)

    if not obj:
        s = _ser(r)
        if s.is_valid():
            s.save(user=r.user)
            return Response(s.data, status=201)
        return Response(s.errors, status=400)

    s = _ser(r, obj, partial=True)
    if s.is_valid():
        s.save()
        return Response(s.data)
    return Response(s.errors, status=400)


@api_view(["POST"])
@permission_classes([IsStudent])
def create_profile(r):
    if StudentProfile.objects.filter(user=r.user).exists():
        return Response({"detail": "Profile already exists; use PATCH"}, status=400)
    s = _ser(r)
    if s.is_valid():
        s.save(user=r.user)
        return Response(s.data, status=201)
    return Response(s.errors, status=400)
