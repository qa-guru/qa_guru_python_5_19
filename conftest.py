import logging
import pytest
import requests
from selene.support.shared import browser

LOGIN = "example1200@example.com"
PASSWORD = "123456"
URL = "https://demowebshop.tricentis.com/login"


def pytest_addoption(parser):
    parser.addoption('--demoqa_url')


@pytest.fixture(scope='session')
def demoqa_url(request):
    return request.config.getoption('--demoqa_url')


@pytest.fixture()
def authorized_cookie():
    response = requests.post(
        url=URL,
        data={"Email": LOGIN, "Password": PASSWORD},
        allow_redirects=False
    )
    logging.info(response.status_code)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    return authorization_cookie


@pytest.fixture()
def authorized_user_browser():
    custom_browser = browser
    response = requests.post(
        url=URL,
        data={"Email": LOGIN, "Password": PASSWORD},
        allow_redirects=False
    )
    logging.info(response.status_code)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    custom_browser.open(URL)
    custom_browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    return custom_browser
