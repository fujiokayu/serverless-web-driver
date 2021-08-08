import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# set directory for AWS Lambda Environment
def move_bin(
    fname: str, src_dir: str = "/var/task/bin", dest_dir: str = "/tmp/bin"
) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_file = os.path.join(dest_dir, fname)
    shutil.copy2(os.path.join(src_dir, fname), dest_file)
    os.chmod(dest_file, 0o775)


def create_driver(
    options: webdriver.chrome.options.Options,
) -> webdriver.chrome.webdriver:
    driver = webdriver.Chrome(
        executable_path="/tmp/bin/chromedriver", chrome_options=options
    )
    return driver

class HeadlessDriver:
    def __init__(self):
        move_bin("headless-chromium")
        move_bin("chromedriver")
        options = webdriver.ChromeOptions()
        options.binary_location = "/tmp/bin/headless-chromium"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--homedir=/tmp")

        self.driver = create_driver(options)

    def set_implicitly_wait(self, seconds):
        self.driver.implicitly_wait(seconds)
    
    def set_explicitly_wait(self, seconds):
        self.wait = WebDriverWait(self.driver, seconds)

    def set_site(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def drag_and_drop(self, source, target):
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target)
        actions.perform()

    def select_by_visible_text(self, text, target):
        select = Select(target)
        select.select_by_visible_text(text)

    def await_alert_accept(self, seconds):
        self.set_explicitly_wait(seconds)
        self.wait.until(expected_conditions.alert_is_present())
        Alert(self.driver).accept()

    def await_element_by_link_text(self, text, seconds):
        return WebDriverWait(self.driver, seconds).until(
            EC.presence_of_element_located((By.LINK_TEXT, text))
        )
