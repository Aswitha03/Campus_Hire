from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsRecruiter, IsRecruiterOrReadOnly
from .models import Company
from .serializers import CompanySerializer


@api_view(["GET", "POST"])
@permission_classes([IsRecruiterOrReadOnly])
def companies(r):
    """Anyone can list companies. A recruiter can create one."""
    if r.method == "GET":
        return Response(CompanySerializer(Company.objects.all(), many=True).data)
    s = CompanySerializer(data=r.data)
    if s.is_valid():
        s.save(recruiter=r.user)
        return Response(s.data, status=201)
    return Response(s.errors, status=400)


@api_view(["GET"])
@permission_classes([IsRecruiter])
def my_companies(r):
    qs = Company.objects.filter(recruiter=r.user)
    return Response(CompanySerializer(qs, many=True).data)
