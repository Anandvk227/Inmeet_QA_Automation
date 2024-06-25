import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

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
        driver = webdriver.Chrome()  # Default to Chrome if no browser specified
        print("Launching Chrome browser as default.........")
    yield driver
    driver.quit()

def pytest_addoption(parser):  # This will get the value from CLI / hooks
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser name e.g. chrome or firefox")
    parser.addoption("--record", action="store_true", help="Enable screen recording")

@pytest.fixture()
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")

@pytest.fixture()
def record(request):
    return request.config.getoption("--record")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "driver":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            test_name = item.nodeid.split("::")[-1]
            file_name = f"{test_name}_Failed_{now.strftime('%H%M%d%m%Y')}.png"
            screenshot_path = Path('Screenshots', file_name)
            driver = item.funcargs.get('driver', None)
            if driver:
                capture_screenshot(driver, str(screenshot_path))
                if screenshot_path.exists():
                    screenshot_full_path = os.path.abspath(str(screenshot_path))
                    html = f'<div><a href="file:///{screenshot_full_path}" target="_blank"><img src="file:///{screenshot_full_path}" alt="Screenshots" style="width:304px;height:228px;" align="right"/></a></div>'
                    extra.append(pytest_html.extras.html(html))
                report.extra = extra

def capture_screenshot(driver, name):
    driver.get_screenshot_as_file(name)

def pytest_html_report_title(report):
    report.title = "InLynk Automation Report"

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now()
    report_dir = Path('Reports', now.strftime("%H%M%d%m%Y"))
    report_dir.mkdir(parents=True, exist_ok=True)
    pytest_html = report_dir / f"report_{now.strftime('%H%M%S')}.html"
    config.option.htmlpath = pytest_html
    config.option.self_contained_html = True

@pytest.fixture(autouse=True)
def record_test(request, record):
    if not record:
        yield
        return

    now = datetime.now().strftime('%H%M%d%m%Y')
    test_name = request.node.name
    video_file = Path('Recordings', f"{test_name}_{now}.mp4")
    video_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        'ffmpeg',
        '-y',  # overwrite output file if it exists
        '-f', 'gdigrab',  # grab the Windows screen
        '-framerate', '30',  # frame rate
        '-i', 'desktop',  # input is the desktop
        '-c:v', 'libx264',  # Use H.264 codec
        '-pix_fmt', 'yuv420p',  # Set pixel format to YUV420P
        '-preset', 'ultrafast',  # Use ultrafast preset for better performance
        str(video_file)
    ]

    print(f"Starting recording with command: {' '.join(command)}")

    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    yield

    process.terminate()
    process.wait()

    if process.returncode:
        print(f"ffmpeg exited with code {process.returncode}", file=sys.stderr)



@pytest.fixture(autouse=True)
def record_test(request, record):
    if not record:
        yield
        return

    now = datetime.now().strftime('%H%M%d%m%Y')
    test_name = request.node.name
    video_file = Path('Recordings', f"{test_name}_{now}.mp4")
    video_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        'ffmpeg',
        '-y',  # overwrite output file if it exists
        '-f', 'gdigrab',  # grab the Windows screen
        '-framerate', '30',  # frame rate
        '-i', 'desktop',  # input is the desktop
        '-c:v', 'libx264',  # Use H.264 codec
        '-pix_fmt', 'yuv420p',  # Set pixel format to YUV420P
        '-preset', 'ultrafast',  # Use ultrafast preset for better performance
        str(video_file)
    ]

    print(f"Starting recording with command: {' '.join(command)}")

    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"ffmpeg output: {output.strip()}", file=sys.stderr)

    rc = process.poll()
    yield
    process.kill()  # Use process.kill() instead of process.terminate()

    if rc:
        print(f"ffmpeg exited with code {rc}", file=sys.stderr)