from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
