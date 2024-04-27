from rest_framework import serializers
from . import models

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = '__all__'