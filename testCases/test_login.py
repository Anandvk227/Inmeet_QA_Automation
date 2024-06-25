
import pytest
from openpyxl.reader.excel import load_workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen

class TestLogin:
    baseURL = ReadConfig.getApplicationURL()

    workbook = load_workbook("TestData/LoginData.xlsx")

    # Access the active worksheet
    worksheet = workbook.active
    username = worksheet["A2"].value
    password = ReadConfig.getPassword()

    workbook.close()

    logger=LogGen.loggen()

    @pytest.mark.run(order=3)
    @pytest.mark.regression
    @pytest.mark.test
    def test_login_Valid_UsernamePassword(self, driver):
        driver.maximize_window()
        self.logger.info("****Opening URL****")
        driver.get(self.baseURL)
        self.logger.info("****Started Login Test****")
        self.logger.info("****TS_1 TC_01 Verify that a registered user can successfully log in with valid credentials.****")
        lp = LoginPage(driver)
        self.logger.info("Entering SuperAdmin Credentials for login Username:" + self.username + " and Password:" + self.password)
        lp.setUserName(self.username)
        # lp.setPassword(self.password)
        lp.clickLogin()
        lp.clickJoinMeeting()
