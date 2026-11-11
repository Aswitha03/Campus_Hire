from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register(r):
    s = RegisterSerializer(data=r.data)
    if s.is_valid():
        user = s.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=201)
    return Response(s.errors, status=400)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login(r):
    user = authenticate(username=r.data.get("username"), password=r.data.get("password"))
    if not user:
        return Response({"detail": "Invalid username or password"}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": UserSerializer(user).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(r):
    return Response(UserSerializer(r.user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(r):
    """Delete the token so it can no longer be used."""
    Token.objects.filter(user=r.user).delete()
    return Response({"detail": "Logged out"})
