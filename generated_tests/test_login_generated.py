import os
from playwright.sync_api import expect


def test_successful_login(page):
    # TC-001: Verify login with valid credentials.
    # Expected: User is redirected to the dashboard.
    page.goto(os.environ.get("LOGIN_PAGE_URL", "https://placeholder.com/login"))
    
    # Use accessible locators for input fields and button
    page.get_by_label(os.environ.get("USERNAME_FIELD_LABEL", "Username")).fill(os.environ.get("VALID_USERNAME", "placeholder_valid_user"))
    page.get_by_label(os.environ.get("PASSWORD_FIELD_LABEL", "Password")).fill(os.environ.get("VALID_PASSWORD", "placeholder_valid_pass"))
    page.get_by_role("button", name=os.environ.get("LOGIN_BUTTON_TEXT", "Log In")).click()
    
    # Assert redirection to the dashboard page
    expect(page).to_have_url(os.environ.get("DASHBOARD_PAGE_URL", "https://placeholder.com/dashboard"))
    # Further assertion to verify a key element on the dashboard page is visible
    expect(page.get_by_role("heading", name=os.environ.get("DASHBOARD_HEADER_TEXT", "Dashboard"))).to_be_visible()


def test_login_with_invalid_credentials(page):
    # TC-002: Verify login with invalid credentials.
    # Expected: An appropriate error message is displayed.
    page.goto(os.environ.get("LOGIN_PAGE_URL", "https://placeholder.com/login"))
    
    # Use accessible locators for input fields and button
    page.get_by_label(os.environ.get("USERNAME_FIELD_LABEL", "Username")).fill(os.environ.get("INVALID_USERNAME", "placeholder_invalid_user"))
    page.get_by_label(os.environ.get("PASSWORD_FIELD_LABEL", "Password")).fill(os.environ.get("INVALID_PASSWORD", "placeholder_invalid_pass"))
    page.get_by_role("button", name=os.environ.get("LOGIN_BUTTON_TEXT", "Log In")).click()
    
    # Assert an appropriate error message is displayed and is visible
    error_message_locator = page.locator(os.environ.get("ERROR_MESSAGE_SELECTOR", ".error-message"))
    expect(error_message_locator).to_be_visible()
    expect(error_message_locator).to_have_text(os.environ.get("INVALID_LOGIN_MESSAGE", "Invalid username or password."))
    
    # Verify that the user remains on the login page or is redirected back to it
    expect(page).to_have_url(os.environ.get("LOGIN_PAGE_URL", "https://placeholder.com/login"))


def test_required_fields_validation(page):
    # TC-003: Verify required email and password fields.
    # Expected: Validation errors are displayed.
    page.goto(os.environ.get("LOGIN_PAGE_URL", "https://placeholder.com/login"))
    
    # Click the login button without entering any credentials to trigger validation
    page.get_by_role("button", name=os.environ.get("LOGIN_BUTTON_TEXT", "Log In")).click()
    
    # Assert that validation error messages are displayed for the username/email field
    username_error_locator = page.locator(os.environ.get("USERNAME_ERROR_SELECTOR", "#username-error"))
    expect(username_error_locator).to_be_visible()
    expect(username_error_locator).to_have_text(os.environ.get("USERNAME_REQUIRED_MESSAGE", "Username is required."))
    
    # Assert that validation error messages are displayed for the password field
    password_error_locator = page.locator(os.environ.get("PASSWORD_ERROR_SELECTOR", "#password-error"))
    expect(password_error_locator).to_be_visible()
    expect(password_error_locator).to_have_text(os.environ.get("PASSWORD_REQUIRED_MESSAGE", "Password is required."))
    
    # Verify that the user remains on the login page after validation errors
    expect(page).to_have_url(os.environ.get("LOGIN_PAGE_URL", "https://placeholder.com/login"))