import requests
from allure import step
from selene.support.conditions import have
from selene.support.shared import browser


LOGIN = "example1200@example.com"
PASSWORD = "123456"


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api(user_cookie):
    response = requests.post(
        "https://demowebshop.tricentis.com/login",
        data={"Email": LOGIN, "Password": PASSWORD},
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("https://demowebshop.tricentis.com/")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("https://demowebshop.tricentis.com/")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api_with_cookie_fixture(authorized_cookie):
    with step("Open shop with authorized user"):
        browser.open("https://demowebshop.tricentis.com/")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorized_cookie})
        browser.open("https://demowebshop.tricentis.com/")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api_with_authorized_user_browser(authorized_user_browser):
    browser = authorized_user_browser

    browser.open("https://demowebshop.tricentis.com/")

    browser.element(".account").should(have.text(LOGIN))
