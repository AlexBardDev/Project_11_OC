"""
This script contains the unit tests of the project.
"""

#External libraries
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

#Local libraries
from food_substitute.models import Bookmark
from .functions import create_new_user, import_data, create_new_bookmark

class ViewsTests(TestCase):
    """This class contains all the tests for the views of this app."""

    def login_user(self):
        """This method logs in a user for a testing purpose."""

        self.client.login(username="test@mail.com", password="passwd")

    def test_home_get(self):
        """This method tests the 'home' view with a GET HTTP method."""

        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_post(self):
        """This method tests the 'home' view with a POST HTTP method."""

        response = self.client.post(reverse('home'), {'research': 'Nutella'})
        assert response.status_code == 302

    def test_search(self):
        """This method tests the 'search' view."""

        import_data()
        response = self.client.get(reverse('search', args=['Nutella']))
        assert response.status_code == 200

    def test_display(self):
        """This method tests the 'display' view."""

        import_data()
        response = self.client.get(reverse('display', args=['Nutella']))
        assert response.status_code == 200

    def test_create_account_get(self):
        """This method tests the 'create_account' view with a GET HTTP
        method."""

        response = self.client.get(reverse('create_account'))
        assert response.status_code == 200

    def test_create_account_post(self):
        """This method tests the 'create_account' view with a POST HTTP
        method."""

        nb_users_1 = User.objects.count()
        response = self.client.post(reverse('create_account'),
                                    {"email": "test.mail@mailtester.com", "password": "passwd"})
        nb_users_2 = User.objects.count()

        assert response.status_code == 302
        assert nb_users_1 + 1 == nb_users_2

    def test_login_get(self):
        """This method tests the 'login' view with a GET HTTP method."""

        response = self.client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_post_wrong_user(self):
        """This method tests the 'login' view with a POST HTTP method and
        a wrong user."""

        response = self.client.post(reverse('login'), {"email": "test@mail.com",
                                                       "password": "passwd", "next":"next"})
        assert response.status_code == 200

    def test_login_post_right_user(self):
        """This method tests the 'login' view with a POST HTTP method and
        a right user."""

        create_new_user()
        response = self.client.post(reverse('login'), {"email": "test@mail.com",
                                                       "password": "passwd", "next": "next"})
        assert response.status_code == 302

    def test_logout(self):
        """This method tests the 'logout' view."""

        response = self.client.get(reverse('logout'))
        assert response.status_code == 302

    def test_bookmark_not_yet_logged(self):
        """This method tests the 'bookmark' view when the user is not yet
        logged."""

        response = self.client.get(reverse('bookmark'))
        assert response.status_code == 302

    def test_bookmark_already_logged(self):
        """This method tests the 'bookmark' view when the user is logged."""

        create_new_user()
        self.login_user()
        response = self.client.get(reverse('bookmark'))
        assert response.status_code == 200

    def test_save_product_not_yet_logged(self):
        """This method tests the 'save_product' view when the user is not yet
        logged."""

        response = self.client.get(reverse('save_product', args=['Pralina', 'Nutella']))
        assert response.status_code == 302

    def test_save_product_already_logged(self):
        """This method tests the 'save_product' view when the user is logged."""

        create_new_user()
        self.login_user()
        import_data()
        response = self.client.get(reverse('save_product', args=['Pralina', 'Nutella']))
        assert response.status_code == 302

    def test_delete_substitute(self):
        """This method tests the 'delete_substitute' view."""

        create_new_user()
        import_data()
        create_new_bookmark()
        self.login_user()

        nb_bookmarks_before = Bookmark.objects.count()
        response = self.client.get(reverse('delete_substitute', args=['Pralina']))
        nb_bookmarks_after = Bookmark.objects.count()

        assert response.status_code == 302
        assert nb_bookmarks_after == nb_bookmarks_before-1

    def test_legal_notices(self):
        """This method tests the 'legal_notices' view."""

        response = self.client.get(reverse('legal_notices'))
        assert response.status_code == 200
