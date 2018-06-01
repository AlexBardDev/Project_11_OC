"""
This script contains all the models of the project.
"""

#Import django libraries
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """This class is the 'Category' table in the database. It stores all the
    categories."""

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class NutritionalInformation(models.Model):
    """This class is the 'NutritionalInformation' table in the database. It
    stores all the nutritional information for 100g."""

    calories = models.PositiveSmallIntegerField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    carbohydrates = models.FloatField()
    sugars = models.FloatField()
    proteins = models.FloatField()
    salt = models.FloatField()
    sodium = models.FloatField()

    def __str__(self):
        return """Informations nutritionelles pour le produit : {}.""".format(
            self.food_set.all()[0].name)

class Food(models.Model):
    """This class is the 'Food' table in the database. It stores all the
    information about food."""

    name = models.CharField(max_length=50)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutriscore = models.CharField(max_length=1)
    id_nutritional_information = models.ForeignKey(NutritionalInformation, on_delete=models.CASCADE)
    image = models.URLField()
    link = models.URLField()

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    """This class is the 'Bookmark' table in the database. It stores all the
    bookmarks of the users."""

    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Food, on_delete=models.CASCADE)

    def __str__(self):
        return """{} a enregistré {}.""".format(self.id_user.username, self.id_product.name)
