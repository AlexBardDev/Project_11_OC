"""
This script customizes the admin interface.
"""
#Import django libraries
from django.contrib import admin
from .models import Food, Category, NutritionalInformation, Bookmark

#Food data
class FoodAdmin(admin.ModelAdmin):
    """This class customizes the 'Food' data for the admin interface."""

    list_display = ('name', 'id_category', 'nutriscore',)
    list_filter = ('nutriscore', 'id_category',)
    search_fields = ('name',)

admin.site.register(Food, FoodAdmin)

#Category data
class CategoryAdmin(admin.ModelAdmin):
    """This class customizes the 'Category' data for the admin interface."""

    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

#NutritionalInformation and Bookmark data
admin.site.register(NutritionalInformation)
admin.site.register(Bookmark)
