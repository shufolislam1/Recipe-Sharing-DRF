from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='media/images')
    ingredients = models.TextField()
    instructions = models.TextField() 
    
# class Ingredient(models.Model):
#     recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     quantity = models.CharField(max_length=50)
#     unit = models.CharField(max_length=50)

# class Instruction(models.Model):
#     recipe = models.ForeignKey(Recipe, related_name='instructions', on_delete=models.CASCADE)
#     step_number = models.PositiveIntegerField()
#     description = models.TextField()