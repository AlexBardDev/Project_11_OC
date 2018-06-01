"""
Here are the url routes of the app.
"""

#Import django libraries
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/<input_user>', views.search, name="search"),
    path('product/<name_product>', views.display, name="display"),
    path('create_account/', views.create_account, name="create_account"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('bookmark/', views.bookmark_user, name="bookmark"),
    path('save_product/<name_product>', views.save_product, name="save_product"),
    path('legal_notices/', views.legal_notices, name="legal_notices"),
]
