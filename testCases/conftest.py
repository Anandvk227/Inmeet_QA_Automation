import os
from datetime import datetime
from pathlib import Path
import subprocess
import base64
import pytest
import zipfile
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import cv2
import numpy as np


class Record:
    def __init__(self, obj, file_name="video", size=None, flags=cv2.IMREAD_COLOR):
        self.obj = obj
        self.flags = flags
        self.size = size
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        if self.size is None:
            self.size = self.get_frame().shape[:2][::-1]
        self.out = cv2.VideoWriter(f"{file_name}.mp4", fourcc, 24.0, self.size)

    def get_frame(self):
        try:
            if isinstance(self.obj, WebDriver):
                im_arr = np.frombuffer(
                    self.obj.get_screenshot_as_png(), dtype=np.uint8)
            elif isinstance(self.obj, WebElement):
                im_arr = np.frombuffer(
                    self.obj.screenshot_as_png, dtype=np.uint8)
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
        self.frame = cv2.imdecode(im_arr, flags=self.flags)
        return self.frame

    def capture(self):
        frame = cv2.resize(self.frame, self.size)
        self.out.write(frame)
        return frame

    def save(self):
        self.out.release()


@pytest.fixture()
def driver(browser):
    if browser == 'chrome':
        driver = webdriver.Chrome()
        print("Launching Chrome browser.........")
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        driver = webdriver.Firefox(options=firefox_options)
        driver.implicitly_wait(30)
        print("Launching Firefox browser.........")
    else:
        driver = webdriver.Chrome()
        print("Launching Chrome browser as default.........")
    yield driver
    driver.quit()


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


def start_screen_recording(test_name, class_name, current_date):
    recording_folder = Path('Recording') / current_date / class_name
    recording_folder.mkdir(parents=True, exist_ok=True)
    file_name = f"{test_name}.mp4"
    recording_path = str(recording_folder / file_name)

    recorder = subprocess.Popen([
        'ffmpeg', '-f', 'gdigrab', '-framerate', '30', '-i', 'desktop', '-c:v', 'libx264', recording_path
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    print(f"Screen recording started. Saving to: {recording_path}")
    return recorder, recording_path


def stop_screen_recording(recorder):
    if recorder:
        recorder.communicate(input=b'q')
        recorder.wait()
        print("Screen recording stopped.")


@pytest.fixture(autouse=True)
def record_screen(request):
    current_date = datetime.now().strftime("%Y-%m-%d")
    if request.config.getoption('--record'):
        test_name = request.node.name
        class_name = request.node.parent.name
        recorder, recording_path = start_screen_recording(test_name, class_name, current_date)
        request.node.recording_path = recording_path
        request.node.recorder = recorder
    yield
    if request.config.getoption('--record'):
        stop_screen_recording(request.node.recorder)
        if request.node.rep_call.passed:
            os.remove(request.node.recording_path)
            print(f"Recording for {test_name} passed and has been removed.")
        else:
            print(f"Recording for {test_name} failed and has been saved.")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    item.rep_call = report

    if report.when == 'call':
        current_date = datetime.now().strftime("%Y-%m-%d")
        pytest_html = item.config.pluginmanager.getplugin('html')
        extra = getattr(report, 'extra', [])

        xfail = hasattr(report, 'wasxfail')
        fail = (report.skipped and xfail) or (report.failed and not xfail)
        if fail:
            test_name = item.nodeid.split("::")[-1]
            class_name = item.nodeid.split("::")[-2]
            screenshot_folder = Path('Screenshots') / current_date / class_name
            screenshot_folder.mkdir(parents=True, exist_ok=True)
            file_name = f"{test_name}_Failed.png"
            screenshot_path = screenshot_folder / file_name

            driver = item.funcargs.get('driver', None)
            if driver:
                capture_screenshot(driver, str(screenshot_path))
                if screenshot_path.exists():
                    with open(screenshot_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()
                    html = f'<div><a href="data:image/png;base64,{encoded_string}" target="_blank"><img src="data:image/png;base64,{encoded_string}" alt="Screenshot" style="width:304px;height:228px;" align="right"/></a></div>'
                    extra.append(pytest_html.extras.html(html))

            recording_path = getattr(item, 'recording_path', None)
            if recording_path:
                if Path(recording_path).exists():
                    with open(recording_path, "rb") as video_file:
                        encoded_video = base64.b64encode(video_file.read()).decode()
                    html = f'''
                                   <div style="margin-top: 10px;">
                                       <a href="data:video/mp4;base64,{encoded_video}" target="_blank" style="display: flex; align-items: center; text-decoration: none;">
                                           <img src="https://img.icons8.com/fluency/48/000000/video.png" alt="Play Video" style="width:30px;height:30px;margin-right:10px;"/>
                                           <span style="font-size: 14px; text-decoration: underline; color: red;">View Video</span>
                                       </a>
                                   </div>'''
                    extra.append(pytest_html.extras.html(html))

            recording_path = getattr(item, 'recording_path', None)
            if recording_path and Path(recording_path).exists():
                video_name = f"{test_name}.mp4"
                zip_path = screenshot_folder / f"{test_name}_report.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    zipf.write(recording_path, arcname=video_name)

                with open(zip_path, "rb") as zip_file:
                    encoded_zip = base64.b64encode(zip_file.read()).decode()

                download_link = f'''
                                <div style="position: absolute; top: 15px; right: 15px;">
                                    <a href="data:application/zip;base64,{encoded_zip}" download="{test_name}_report.zip" style="color: blue;">
                                        <img src="https://img.icons8.com/?size=30&id=110690&format=png&color=FFAA00" alt="Download Icon" style="vertical-align: middle;" />
                                        Download Report
                                    </a>
                                </div>
                                '''
                extra.append(pytest_html.extras.html(download_link))

        report.extra = extra


def capture_screenshot(driver, name):
    driver.get_screenshot_as_file(name)


def pytest_html_report_title(report):
    report.title = "InLynk Automation Report"


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser name e.g. chrome or firefox")
    parser.addoption("--record", action="store_true", help="Enable screen recording during tests")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    current_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%I_%M_%p")
    report_folder = Path('Reports') / current_date
    report_folder.mkdir(parents=True, exist_ok=True)
    pytest_html = report_folder / f"report_{now_time}.html"
    config.option.htmlpath = pytest_html
    config.option.self_contained_html = True
