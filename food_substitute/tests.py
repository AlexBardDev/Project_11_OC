"""
This script contains all the tests of the project.
"""

#External libraries
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

#Local library
from .models import Food, Category, NutritionalInformation

class ViewsTests(TestCase):
    """This class contains all the tests for the views of this app."""

    def setUp(self):
        """This method is called before each test."""

        pass

    def new_food(self):
        """This function creates new rows in the database."""

        new_category = Category.objects.create(name="produits-a-tartiner")

        nutri_product = NutritionalInformation.objects.create(calories=539,
                                                              fat=30, saturated_fat=10,
                                                              carbohydrates=57, sugars=56,
                                                              proteins=6, salt=0, sodium=0)
        product = Food.objects.create(name="Nutella", nutriscore="e",
                                      image="https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.87.400.jpg",
                                      link="https://fr.openfoodfacts.org/produit/3017620421006/nutella-ferrero",
                                      id_category=new_category, id_nutritional_information=nutri_product)

        nutri_substitute = NutritionalInformation.objects.create(calories=539,
                                                                 fat=31, saturated_fat=5,
                                                                 carbohydrates=57, sugars=55,
                                                                 proteins=5, salt=0, sodium=0)
        substitute = Food.objects.create(name="Pralina", nutriscore="d",
                                         image="https://static.openfoodfacts.org/images/products/326/385/223/1719/front_fr.24.400.jpg",
                                         link="https://fr.openfoodfacts.org/produit/3263852231719/pralina-leader-price",
                                         id_category=new_category, id_nutritional_information=nutri_substitute)

    def create_user(self):
        """This function creates a new user for a testing purpose."""

        User.objects.create_user("test@mail.com", "test@mail.com", "passwd")

    def login_user(self):
        """This function logs in a user for a testing purpose."""

        self.client.login(username="test@mail.com", password="passwd")

    def test_home_get(self):
        """This function tests the 'home' view with a GET HTTP method."""

        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_post(self):
        """This function tests the 'home' view with a POST HTTP method."""

        response = self.client.post(reverse('home'), {'research': 'Nutella'})
        assert response.status_code == 302

    def test_search(self):
        """This function tests the 'search' view."""

        self.new_food()
        response = self.client.get(reverse('search', args=['Nutella']))
        assert response.status_code == 200

    def test_display(self):
        """This function tests the 'display' view."""

        self.new_food()
        response = self.client.get(reverse('display', args=['Nutella']))
        assert response.status_code == 200

    def test_create_account_get(self):
        """This function tests the 'create_account' view with a GET HTTP
        method."""

        response = self.client.get(reverse('create_account'))
        assert response.status_code == 200

    def test_create_account_post(self):
        """This function tests the 'create_account' view with a POST HTTP
        method."""

        nb_users_1 = User.objects.count()
        response = self.client.post(reverse('create_account'),
                                    {"email": "test.mail@mailtester.com", "password": "passwd"})
        nb_users_2 = User.objects.count()

        assert response.status_code == 302
        assert nb_users_1 + 1 == nb_users_2

    def test_login_get(self):
        """This function tests the 'login' view with a GET HTTP method."""

        response = self.client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_post_wrong_user(self):
        """This function tests the 'login' view with a POST HTTP method and
        a wrong user."""

        response = self.client.post(reverse('login'), {"email": "test@mail.com",
                                                       "password": "passwd", "next":"next"})
        assert response.status_code == 200

    def test_login_post_right_user(self):
        """Thus function tests the 'login' view with a POST HTTP method and
        a right user."""

        self.create_user()
        response = self.client.post(reverse('login'), {"email": "test@mail.com",
                                                       "password": "passwd", "next": "next"})
        assert response.status_code == 302

    def test_logout(self):
        """This function tests the 'logout' view."""

        response = self.client.get(reverse('logout'))
        assert response.status_code == 302

    def test_bookmark_not_yet_logged(self):
        """This function tests the 'bookmark' view when the user is not yet
        logged."""

        response = self.client.get(reverse('bookmark'))
        assert response.status_code == 302

    def test_bookmark_already_logged(self):
        """This function tests the 'bookmark' view when the user is logged."""

        self.create_user()
        self.login_user()
        response = self.client.get(reverse('bookmark'))
        assert response.status_code == 200

    def test_save_product_not_yet_logged(self):
        """This function tests the 'save_product' view when the user is not yet
        logged."""

        response = self.client.get(reverse('save_product', args=['Nutella']))
        assert response.status_code == 302

    def test_save_product_already_logged(self):
        """This function tests the 'save_product' view when the user is logged."""

        self.create_user()
        self.login_user()
        self.new_food()
        response = self.client.get(reverse('save_product', args=['Nutella']))
        assert response.status_code == 302

    def test_legal_notices(self):
        """This function tests the 'legal_notices' view."""

        response = self.client.get(reverse('legal_notices'))
        assert response.status_code == 200

class IntegrationTests(StaticLiveServerTestCase):
    """This class contains all the integration tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def import_data(self):
        """This method imports some data in the database."""

        new_category = Category.objects.create(name="produits-a-tartiner")

        nutri_product = NutritionalInformation.objects.create(calories=539,
                                                              fat=30, saturated_fat=10,
                                                              carbohydrates=57, sugars=56,
                                                              proteins=6, salt=0, sodium=0)
        product = Food.objects.create(name="Nutella", nutriscore="e",
                                      image="https://static.openfoodfacts.org/images/products/301/762/042/1006/front_fr.87.400.jpg",
                                      link="https://fr.openfoodfacts.org/produit/3017620421006/nutella-ferrero",
                                      id_category=new_category, id_nutritional_information=nutri_product)

        nutri_substitute = NutritionalInformation.objects.create(calories=539,
                                                                 fat=31, saturated_fat=5,
                                                                 carbohydrates=57, sugars=55,
                                                                 proteins=5, salt=0, sodium=0)
        substitute = Food.objects.create(name="Pralina", nutriscore="d",
                                         image="https://static.openfoodfacts.org/images/products/326/385/223/1719/front_fr.24.400.jpg",
                                         link="https://fr.openfoodfacts.org/produit/3263852231719/pralina-leader-price",
                                         id_category=new_category, id_nutritional_information=nutri_substitute)

    def create_new_user(self):
        """This method creates a new user in the database."""

        User.objects.create_user("test@mail.com", "test@mail.com", "passwd")

    def test_get_home_page_do_a_research_and_see_a_product(self):
        """This test gets the home page. Then, submits a form and does a
        research. And finally, displays the product page."""

        self.import_data()
        self.selenium.get(self.live_server_url)
        search_input = self.selenium.find_element_by_css_selector("#about input[type='search']")
        search_input.send_keys("Nutella")
        self.selenium.find_element_by_class_name("btn-outline-primary").click()
        self.selenium.find_element_by_css_selector(".row a[href*='/product/']").click()
        content = self.selenium.find_element_by_css_selector("a[target='_blank']")
        assert content.text == "Voir la fiche complète d'OpenFoodFacts"

    def test_create_new_account(self):
        """This test gets the 'create account' page and simulates a new user."""

        self.selenium.get(self.live_server_url + "/create_account/")
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys("test@mail.com")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("passwd")
        self.selenium.find_element_by_css_selector("input[type='submit']").click()
        content = self.selenium.find_element_by_class_name("special_message")
        assert content.text == "Votre compte a été créé avec succès et vous êtes maintenant connecté."

    def test_login_bookmarks_and_logout(self):
        """This test gets the 'login' page. It simulates a user that logs in,
        does a research, saves a new substitute, sees the bookmarks page and
        logs out."""

        self.import_data()
        self.create_new_user()

        self.selenium.get(self.live_server_url + "/login/")
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys("test@mail.com")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("passwd")
        self.selenium.find_element_by_css_selector("input[type='submit']").click()

        search_input = self.selenium.find_element_by_css_selector("#about input[type='search']")
        search_input.send_keys("Nutella")
        self.selenium.find_element_by_class_name("btn-outline-primary").click()

        substitute_name = self.selenium.find_element_by_css_selector(".row a p").text
        self.selenium.find_element_by_css_selector(".row p a").click()

        self.selenium.find_element_by_css_selector("nav a[href*='/bookmark/']").click()
        product_name = self.selenium.find_element_by_css_selector("a p").text

        self.selenium.find_element_by_css_selector("nav a[href*='/logout/']").click()

        assert substitute_name == product_name
