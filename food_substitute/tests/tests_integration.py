"""
This script contains all the integration tests.
"""

#External libraries
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

#Local library
from .functions import create_new_user, import_data, create_new_bookmark

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

    def test_get_home_page_do_a_research_and_see_a_product(self):
        """This test gets the home page. Then, submits a form and does a
        research. And finally, displays the product page."""

        import_data()
        self.selenium.get(self.live_server_url)
        search_input = self.selenium.find_element_by_css_selector("#about input[type='search']")
        search_input.send_keys("Nutella")
        self.selenium.find_element_by_class_name("btn-outline-primary").click()
        self.selenium.find_element_by_css_selector(".row a[href*='/product/']").click()
        content = self.selenium.find_element_by_css_selector("a[target='_blank']")
        assert content.text == "Voir la fiche complète sur OpenFoodFacts"

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

        import_data()
        create_new_user()

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

    def test_remove_substitute(self):
        """The user is already logged, sees the saved substitutes and removes
        one of them."""

        import_data()
        create_new_user()
        create_new_bookmark()

        #Login the user and get the 'bookmark' page
        self.client.login(username="test@mail.com", password="passwd")
        cookie = self.client.cookies['sessionid']
        self.selenium.get(self.live_server_url + "/bookmark/")
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                  'secure': False, 'path': '/'})
        self.selenium.refresh()

        self.selenium.get(self.live_server_url + "/bookmark/")
        self.selenium.find_element_by_css_selector("button[data-toggle='modal']").click()
        self.selenium.find_element_by_css_selector(".modal-body a").click()
        content = self.selenium.find_element_by_css_selector(".special_message")

        assert content.text == "Substitut supprimé"
