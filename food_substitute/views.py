"""
This script contains all the views of my app.
"""

#Standard library
import re
from operator import attrgetter

#Import django libraries
from django.shortcuts import render, redirect
from .models import Food, Bookmark
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages

def home(request):
    """This view returns the home of the web site."""

    if request.method == "POST":
        input_user = request.POST.get("research")
        return redirect("search", input_user)
    else:
        return render(request, "food_substitute/home.html")

def search(request, input_user):
    """This view searches a healthier substitute and shows the results."""

    result = Food.objects.filter(name__icontains=input_user)

    if len(result) == 0:
        #Find some suggestions with a regex
        list_suggestions = [food for food in Food.objects.all() if re.search(input_user, food.name)]
        if len(list_suggestions) != 0:
            context = {"product": input_user, "list_suggestions":list_suggestions}
            return render(request, "food_substitute/suggestion.html", context)
        else:
            context = {"product":input_user}
            return render(request, "food_substitute/not_found.html", context)
    else:
        result = result[0]
        #Food with same category but better nutriscore
        list_substitute = [food for food in Food.objects.filter(id_category=result.id_category)
                           if ord(food.nutriscore) < ord(result.nutriscore)]
        #Pagination if necessary
        if len(list_substitute) > 6:
            paginator = Paginator(list_substitute, 6)
            page = request.GET.get('page')
            list_substitute = paginator.get_page(page)

        context = {"product":result, "list_substitute": list_substitute}

        return render(request, "food_substitute/search.html", context)

def display(request, name_product):
    """This view displays the information about a selected product."""

    product = Food.objects.filter(name=name_product)[0]

    context = {"product": product, "list_letters":["A", "B", "C", "D", "E"]}

    return render(request, "food_substitute/display.html", context)

def login_user(request):
    """This view allows the connexion of the users."""

    if request.method == "POST":
        #Get the data
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next")

        #Login and redirection to the good url
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Vous êtes maintenant connecté !")

            if next_url == "/bookmark/":
                return redirect("bookmark")
            elif "/search/" in next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect("home")
        else:
            messages.add_message(request, messages.WARNING,
                                 "Mauvais email ou mauvais mot de passe.")
            return render(request, "food_substitute/login.html", {"next": next_url})
    else:
        #Save the previous url for a future redirection
        next_url = request.GET.get("next")
        if next_url is not None and "/save_product/" in next_url:
            next_url = request.META.get('HTTP_REFERER')

        return render(request, "food_substitute/login.html", {"next": next_url})

def create_account(request):
    """This view creates a user account."""

    if request.method == "POST":
        #Get the data
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(User.objects.filter(username=email)) != 0:
            messages.add_message(request, messages.WARNING, "Votre compte existe déjà.")
        else:
            #Create a new user and login automatically
            User.objects.create_user(email, email, password)
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                messages.add_message(request, messages.SUCCESS,
                                     "Votre compte a été créé avec succès et vous êtes maintenant connecté.")

        return redirect("home")
    else:
        return render(request, "food_substitute/account.html")

def logout_user(request):
    """This view logs out a user."""

    logout(request)
    messages.add_message(request, messages.SUCCESS, "Vous êtes déconnecté.")
    return redirect("home")

@login_required
def bookmark_user(request):
    """This view returns all the saved substitutes of the user."""

    list_bookmarks = Bookmark.objects.filter(id_user=request.user.id)

    if list_bookmarks:
        list_original_products = list(set([bookmark.id_original_product for bookmark in list_bookmarks])) 
        new_list_bookmarks = []
        for i in range(len(list_original_products)):
            new_list = []
            for bookmark in list_bookmarks:
                if bookmark.id_original_product == list_original_products[i]:
                    new_list.append(bookmark)
            new_list_bookmarks.append(new_list)
        context = {"list_bookmarks": new_list_bookmarks}
    else:
        context = {"list_bookmarks": list_bookmarks}

    return render(request, "food_substitute/bookmark.html", context)

@login_required
def save_product(request, name_substitute, name_product):
    """This view saves a new bookmark for the current user."""

    substitute = Food.objects.filter(name=name_substitute)[0]
    product = Food.objects.filter(name=name_product)[0]
    user = request.user

    #Create a new bookmark
    if Bookmark.objects.filter(id_substitute=substitute.id):
        messages.add_message(request, messages.SUCCESS, "Ce substitut est déjà enregistré.")
    else:
        Bookmark.objects.create(id_user=user, id_substitute=substitute, id_original_product=product)
        messages.add_message(request, messages.SUCCESS, "Substitut sauvegardé avec succès !")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_substitute(request, name_substitute):
    """This view removes a bookmark for the current user."""

    substitute = Food.objects.filter(name=name_substitute)[0]
    Bookmark.objects.filter(id_user=request.user.id, id_substitute=substitute.id).delete()

    messages.add_message(request, messages.SUCCESS, "Substitut supprimé.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def legal_notices(request):
    """This view returns the legal notices page."""

    return render(request, "food_substitute/legal_notices.html")
