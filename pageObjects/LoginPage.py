import time
# from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # Login Page
    textbox_username_id = "email"
    textbox_password_id = "password"
    button_login_xpath = "//button[normalize-space()='Login']"

    button_JoinMeeting_xpath = "//div[@class='dashBtn dashGreebBg']"


    def __init__(self,driver):
        self.driver=driver

    def setUserName(self, username):
        # Wait for the text box element to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, self.textbox_username_id))
        )

        # Find the text box element and perform actions
        textbox = self.driver.find_element(By.ID, self.textbox_username_id)
        textbox.clear()
        textbox.send_keys(username)


    def setPassword(self, password):
        self.driver.find_element(By.ID, self.textbox_password_id).clear()
        self.driver.find_element(By.ID, self.textbox_password_id).send_keys(password)

    def clickLogin(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, self.button_login_xpath)))
        element.click()



    def clickJoinMeeting(self):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, self.button_JoinMeeting_xpath)))
        element.click()

