import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time


SHORT_WAIT_TIME = 3
MID_WAIT_TIME = 5
LONG_WAIT_TIME = 10


def login_salonboard(driver, user_id, password):

    driver.get('https://salonboard.com/login/')

    try:
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "idPasswordInputForm"))
        )
    except TimeoutError as e:
        driver.quit()
        return

    userIdInput = driver.find_element(By.XPATH, "//input[@name='userId']")  


    for letter in user_id:
        userIdInput.send_keys(letter)
        # time.sleep(0.5)

    passwordInput = driver.find_element(By.XPATH, "//input[@name='password']")  


    for letter in password:
        passwordInput.send_keys(letter)
        # time.sleep(0.5)

    WebDriverWait(driver, SHORT_WAIT_TIME)

    loginButton = driver.find_element(By.XPATH, "//a[@class='input_area_btn_01']")
    loginButton.click()


    return driver