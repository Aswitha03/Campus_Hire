from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsRecruiter, IsRecruiterOrReadOnly, get_role
from applications.models import Application
from companies.models import Company
from .models import Job
from .serializers import JobSerializer


def build_context(r):
    """Extra info so students see 'eligible' and 'applied' on every job."""
    ctx = {"request": r, "is_student": False}
    if get_role(r.user) == "student":
        ctx.update(
            is_student=True,
            profile=getattr(r.user, "student_profile", None),
            applied_ids=set(Application.objects.filter(student=r.user).values_list("job_id", flat=True)),
        )
    return ctx


@api_view(["GET", "POST"])
@permission_classes([IsRecruiterOrReadOnly])
def jobs(r):
    """GET active jobs (optional ?q=search&min_package=5). POST creates a job (recruiter)."""
    if r.method == "GET":
        qs = Job.objects.filter(is_active=True).select_related("company").order_by("-id")
        q = r.query_params.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(company__name__icontains=q)
                | Q(required_skills__icontains=q) | Q(location__icontains=q)
            )
        try:
            if r.query_params.get("min_package"):
                qs = qs.filter(package_lpa__gte=float(r.query_params["min_package"]))
        except ValueError:
            pass
        return Response(JobSerializer(qs, many=True, context=build_context(r)).data)

    try:
        company = Company.objects.get(id=r.data.get("company"), recruiter=r.user)
    except (Company.DoesNotExist, ValueError, TypeError):
        return Response({"detail": "Company not found for this recruiter"}, status=400)
    s = JobSerializer(data=r.data, context=build_context(r))
    if s.is_valid():
        s.save(company=company)
        return Response(s.data, status=201)
    return Response(s.errors, status=400)


@api_view(["GET"])
@permission_classes([IsRecruiter])
def my_jobs(r):
    """All jobs (active and closed) of the logged-in recruiter, with applicant counts."""
    qs = (Job.objects.filter(company__recruiter=r.user)
          .select_related("company").annotate(applications_count=Count("applications")).order_by("-id"))
    return Response(JobSerializer(qs, many=True).data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsRecruiterOrReadOnly])
def job_detail(r, pk):
    job = get_object_or_404(Job.objects.select_related("company"), pk=pk)
    if r.method == "GET":
        return Response(JobSerializer(job, context=build_context(r)).data)
    if job.company.recruiter_id != r.user.id:
        return Response({"detail": "You can only change your own jobs"}, status=403)
    if r.method == "DELETE":
        job.delete()
        return Response(status=204)
    s = JobSerializer(job, data=r.data, partial=True)
    if s.is_valid():
        s.save()
        return Response(s.data)
    return Response(s.errors, status=400)
