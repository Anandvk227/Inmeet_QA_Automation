import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import logging

class TestLogin:

    baseURL = "https://testapp.inmeet.ai/inconf/668e13e8db3bf224d36c7355/ZmFsc2U="
    chrome_driver_path = './drivers/chromedriver.exe'
    firefox_driver_path = './drivers/geckodriver.exe'

    @pytest.fixture(scope="class")
    def setup(self):
        # Initialize logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # Host in regular Chrome window
        chrome_service = Service(self.chrome_driver_path)
        chrome_options = Options()
        self.host_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # Participant 1 in Incognito mode
        options_incognito = Options()
        options_incognito.add_argument("--incognito")
        self.participant1_driver = webdriver.Chrome(service=chrome_service, options=options_incognito)

        # Participant 2 in Firefox
        firefox_service = FirefoxService(self.firefox_driver_path)
        firefox_options = FirefoxOptions()
        self.participant2_driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

        # Participant 3 in another Incognito Chrome
        self.participant3_driver = webdriver.Chrome(service=chrome_service, options=options_incognito)

        yield
        self.host_driver.quit()
        self.participant1_driver.quit()
        self.participant2_driver.quit()
        self.participant3_driver.quit()

    def join_conference(self, driver, username):
        # Locate and fill the username input field
        username_field = driver.find_element(By.ID, "displayname")
        username_field.send_keys(username)
        # Click the join button
        join_button = driver.find_element(By.ID, "joinButton")
        join_button.click()

    def perform_host_actions(self, driver):
        # Example action: Mute/Unmute
        mute_button = driver.find_element(By.ID, 'mute-button-id')
        mute_button.click()

    def perform_participant_actions(self, driver):
        # Example action: Raise Hand
        raise_hand_button = driver.find_element(By.ID, 'raise-hand-button-id')
        raise_hand_button.click()

    @pytest.mark.run(order=1)
    @pytest.mark.regression
    def test_homePageTitle(self, setup):
        self.host_driver.maximize_window()
        self.logger.info("**** Opening URL ****")
        self.host_driver.get(self.baseURL)
        self.participant1_driver.get(self.baseURL)
        self.participant2_driver.get(self.baseURL)
        self.participant3_driver.get(self.baseURL)

    @pytest.mark.run(order=2)
    @pytest.mark.regression
    def test_join_conference(self, setup):
        self.join_conference(self.host_driver, "Host")
        self.join_conference(self.participant1_driver, "Participant 1")
        self.join_conference(self.participant2_driver, "Participant 2")
        self.join_conference(self.participant3_driver, "Participant 3")

    @pytest.mark.run(order=3)
    @pytest.mark.regression
    def test_perform_actions(self, setup):
        self.perform_host_actions(self.host_driver)
        self.perform_participant_actions(self.participant1_driver)
