"""
This script contains some functions used for the tests.
"""

#External library
from django.contrib.auth.models import User

#Local library
from food_substitute.models import Food, Category, NutritionalInformation, Bookmark

def create_new_user():
    """This function creates a new user in the database."""

    User.objects.create_user("test@mail.com", "test@mail.com", "passwd")

def import_data():
    """This function imports some data in the database."""

    new_category = Category.objects.create(name="produits-a-tartiner")

    nutri_product = NutritionalInformation.objects.create(calories=539,
                                                          fat=30, saturated_fat=10,
                                                          carbohydrates=57, sugars=56,
                                                          proteins=6, salt=0, sodium=0)
    Food.objects.create(name="Nutella", nutriscore="e",
                        image="https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.87.400.jpg",
                        link="https://fr.openfoodfacts.org/produit/3017620421006/nutella-ferrero",
                        id_category=new_category, id_nutritional_information=nutri_product)

    nutri_substitute = NutritionalInformation.objects.create(calories=539,
                                                             fat=31, saturated_fat=5,
                                                             carbohydrates=57, sugars=55,
                                                             proteins=5, salt=0, sodium=0)
    Food.objects.create(name="Pralina", nutriscore="d",
                        image="https://static.openfoodfacts.org/images/products/326/385/223/1719/front_fr.24.400.jpg",
                        link="https://fr.openfoodfacts.org/produit/3263852231719/pralina-leader-price",
                        id_category=new_category, id_nutritional_information=nutri_substitute)

def create_new_bookmark():
    """This function creates a new bookmark in the database."""

    user = User.objects.filter(username="test@mail.com")[0]
    substitute = Food.objects.filter(name="Pralina")[0]
    product = Food.objects.filter(name="Nutella")[0]

    Bookmark.objects.create(id_user=user, id_substitute=substitute, id_original_product=product)


