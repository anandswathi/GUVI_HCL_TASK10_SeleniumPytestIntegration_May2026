"""
Pytest Test Suite — saucedemo.com (Task 10)
============================================
Positive & Negative test-cases for:
  1. Title of the web application
  2. URL of the Homepage
  3. URL of the Dashboard after Login
"""
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Constants
BASE_URL             = "https://www.saucedemo.com/"
DASHBOARD_URL        = "https://www.saucedemo.com/inventory.html"
EXPECTED_TITLE       = "Swag Labs"
VALID_USERNAME       = "standard_user"
VALID_PASSWORD       = "secret_sauce"
INVALID_USERNAME     = "wrong_user"
INVALID_PASSWORD     = "wrong_password"

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Provide a driver that is already logged into the dashboard.
    """
    driver.get(BASE_URL)
    driver.maximize_window()
    driver.find_element(By.ID, "user-name").send_keys(VALID_USERNAME)
    driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    return driver

# Test cases for the title of the web application.
def test_positive_title_on_homepage(driver):
    """
    POSITIVE: Title on the homepage should be 'Swag Labs'.
    """
    driver.get(BASE_URL)
    assert driver.title == EXPECTED_TITLE, (
             f"Expected title: '{EXPECTED_TITLE}', Actual title: '{driver.title}'"
    )

def test_positive_title_on_dashboard(logged_in_driver):
    """
    POSITIVE: Title on the dashboard should remain 'Swag Labs' after login.
    """
    assert logged_in_driver.title == EXPECTED_TITLE, (
             f"Expected title '{EXPECTED_TITLE}', Actual title: '{logged_in_driver.title}'"
    )

def test_positive_title_on_dashboard_after_continuous_refresh(logged_in_driver):
    """
    POSITIVE: Title on the dashboard should be 'Swag Labs' after multiple page refresh.
    """
    logged_in_driver.get(BASE_URL)
    for i in range(10):
        logged_in_driver.refresh()

    assert logged_in_driver.title == EXPECTED_TITLE, (
             f"Expected title: '{EXPECTED_TITLE}', Actual title: '{logged_in_driver.title}'"
    )

def test_negative_title_not_blank(driver):
     """
     NEGATIVE: Page title must not be empty.
     """
     driver.get(BASE_URL)
     assert driver.title != "", "Page title should not be empty."


#============================================================================================

# Test cases for the URL of the homepage (login page)
def test_positive_homepage_url_match_curr_url(driver):
    """
    POSITIVE: Homepage URL should exactly match the base/current URL.
    """
    driver.get(BASE_URL)
    assert driver.current_url == BASE_URL, (
            f"Expected: '{BASE_URL}', Actual: '{driver.current_url}'"
    )

def test_positive_homepage_url_uses_https(driver):
    """
    POSITIVE: Homepage URL should use HTTPS.
    """
    driver.get(BASE_URL)
    assert driver.current_url.startswith("https://"), (
            "Homepage URL must use HTTPS."
    )

def test_negative_homepage_url_not_dashboard_url(driver):
    """
    NEGATIVE: Navigating to homepage should NOT land on dashboard.
    """
    driver.get(BASE_URL)
    assert "inventory" not in driver.current_url, (
            "Homepage URL must not contain 'inventory' — user should not be auto-logged in."
    )

def test_negative_homepage_url_not_wrong_domain(driver):
    """
    NEGATIVE: Homepage URL must not belong to a different domain.
    """
    driver.get(BASE_URL)
    assert "saucedemo.com" in driver.current_url, (
            "Unexpected domain — URL does not belong to saucedemo.com."
    )

#============================================================================================

# Test cases for the URL of the Dashboard after Login
def test_positive_dashboard_url_after_valid_login(logged_in_driver):
    """
    POSITIVE: Valid login should redirect to inventory/dashboard page.
    """
    assert logged_in_driver.current_url == DASHBOARD_URL, (
            f"Expected: '{DASHBOARD_URL}', Actual: '{logged_in_driver.current_url}'"
    )

def test_positive_dashboard_url_contains_inventory(logged_in_driver):
    """
    POSITIVE: Dashboard URL must contain 'inventory'.
    """
    assert "inventory" in logged_in_driver.current_url, (
            "Dashboard URL should contain 'inventory' after login."
    )

def test_negative_invalid_login_stays_on_homepage(driver):
    """
    NEGATIVE: Invalid credentials should NOT redirect to dashboard.
    """
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(INVALID_USERNAME)
    driver.find_element(By.ID, "password").send_keys(INVALID_PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    # Should remain on login page — NOT navigate to inventory
    assert "inventory" not in driver.current_url, (
            "Invalid credentials should not grant dashboard access."
    )

def test_negative_direct_dashboard_access_without_login(driver):
    """
    NEGATIVE: Accessing dashboard URL directly without login should redirect back to login.
    """
    driver.get(DASHBOARD_URL)
    time.sleep(2)
    # saucedemo redirects unauthenticated users back to the base login page
    assert driver.current_url == BASE_URL, (
        f"Unauthenticated access to dashboard should redirect to '{BASE_URL}', "
        f"but landed on '{driver.current_url}'"
    )