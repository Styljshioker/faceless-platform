"""E2E tests using Selenium for browser automation."""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    """Create Selenium WebDriver."""
    driver = webdriver.Chrome()  # or webdriver.Firefox()
    yield driver
    driver.quit()


def test_user_registration_e2e(driver):
    """Test user registration E2E."""
    driver.get("http://localhost:3000")
    
    # Wait for register button
    register_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Register here"))
    )
    register_button.click()
    
    # Fill registration form
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("test@example.com")
    
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("testuser")
    
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("securepassword123")
    
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    # Wait for success message
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()


def test_content_creation_e2e(driver):
    """Test content creation E2E."""
    driver.get("http://localhost:3000/login")
    
    # Login
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("test@example.com")
    
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("securepassword123")
    
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    # Wait for dashboard
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )
    
    # Navigate to content creation
    content_link = driver.find_element(By.LINK_TEXT, "Create Content")
    content_link.click()
    
    # Fill content form
    title_input = driver.find_element(By.ID, "title")
    title_input.send_keys("Test Video")
    
    script_input = driver.find_element(By.ID, "script")
    script_input.send_keys("This is a test script for video generation.")
    
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    # Wait for success
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()
