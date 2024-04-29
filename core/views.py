from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from . import models
from . import serializers
# Create your views here.

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
