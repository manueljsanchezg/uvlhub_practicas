import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_prueba_notepad():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        driver.get(f"{host}/")
        driver.set_window_size(847, 779)
        time.sleep(4)

        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(4)

        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")
        driver.find_element(By.ID, "submit").click()
        time.sleep(4)
        
        driver.get(f"{host}/notepad")
        time.sleep(4)

        driver.find_element(By.LINK_TEXT, "Create").click()
        time.sleep(4)
        title_field = driver.find_element(By.ID, "title")
        body_field = driver.find_element(By.ID, "body")
        title_field.send_keys("nueva nota")
        title_field.send_keys(Keys.DOWN)
        title_field.send_keys("nueva nota")
        body_field.send_keys("body")
        driver.find_element(By.ID, "submit").click()
        time.sleep(4)

        driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) > a:nth-child(2)").click()
        time.sleep(4)
        title_field = driver.find_element(By.ID, "title")
        title_field.click()
        title_field.send_keys("nueva nota 2")
        driver.find_element(By.ID, "submit").click()
        time.sleep(4)

        driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) button").click()
        time.sleep(4)

        print("Test completed successfully!")

    finally:
        close_driver(driver)


test_prueba_notepad()
