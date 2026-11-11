from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsRecruiter, IsStudent
from jobs.models import Job
from .models import Application
from .serializers import ApplicationSerializer

RELATED = ("student", "student__student_profile", "job", "job__company")


@api_view(["POST"])
@permission_classes([IsStudent])
def apply(r, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    profile = getattr(r.user, "student_profile", None)
    if not profile:
        return Response({"detail": "Complete your student profile first"}, status=400)
    ok, reason = job.check_eligibility(profile)
    if not ok:
        return Response({"detail": f"You are not eligible for this job. {reason}"}, status=400)
    obj, created = Application.objects.get_or_create(student=r.user, job=job)
    if not created:
        return Response({"detail": "Already applied"}, status=400)
    return Response(ApplicationSerializer(obj, context={"request": r}).data, status=201)


@api_view(["GET"])
@permission_classes([IsStudent])
def mine(r):
    qs = Application.objects.filter(student=r.user).select_related(*RELATED).order_by("-applied_at")
    return Response(ApplicationSerializer(qs, many=True, context={"request": r}).data)


@api_view(["DELETE"])
@permission_classes([IsStudent])
def withdraw(r, pk):
    """A student can withdraw only while the status is still 'applied'."""
    obj = get_object_or_404(Application, pk=pk, student=r.user)
    if obj.status != "applied":
        return Response({"detail": "Only applications in 'applied' status can be withdrawn"}, status=400)
    obj.delete()
    return Response(status=204)


@api_view(["GET", "PATCH"])
@permission_classes([IsRecruiter])
def recruiter(r):
    """GET applicants for my jobs (?job=<id> to filter). PATCH {application_id, status}."""
    qs = Application.objects.filter(job__company__recruiter=r.user).select_related(*RELATED).order_by("-applied_at")
    ctx = {"request": r}
    if r.method == "GET":
        if r.query_params.get("job"):
            qs = qs.filter(job_id=r.query_params["job"])
        return Response(ApplicationSerializer(qs, many=True, context=ctx).data)

    try:
        obj = qs.get(id=r.data.get("application_id"))
    except (Application.DoesNotExist, ValueError, TypeError):
        return Response({"detail": "Application not found"}, status=404)
    status = r.data.get("status")
    if status not in ["shortlisted", "rejected", "selected"]:
        return Response({"detail": "Invalid status"}, status=400)
    obj.status = status
    obj.save(update_fields=["status"])
    return Response(ApplicationSerializer(obj, context=ctx).data)
