from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

class StravaLogin:
    def __init__(self, username, password, geckodriver_path='/Users/rahuljois/Downloads/geckodriver',url = 'https://www.strava.com/login/'):
        self.username = username
        self.password = password
        self.geckodriver_path = geckodriver_path
        self.url = url 
        self.driver = None
        self.delay = 5

    def login(self):
        #Initiate Firefox Options and open URL
        firefox_options = Options()
        firefox_options.add_argument('--window-size=1920x1080') 
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        firefox_options.add_argument('user-agent={0}'.format(user_agent))
        self.driver = webdriver.Firefox(executable_path=self.geckodriver_path, options=firefox_options)
        self.driver.get(self.url)

        #Find email and password XPaths and enter email and password
        enter_email_element = self.driver.find_element("xpath", "//*[@id='email']")
        enter_email_element.send_keys(self.username)
        password_element = self.driver.find_element("xpath", "//*[@id='password']")
        password_element.send_keys(self.password)
        
        #Click Login Button
        button = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.ID, "login-button")))
        button.click()

    def get_driver(self):
        return self.driver


strava_login = StravaLogin('', '')
strava_login.login()
driver = strava_login.get_driver()
print(driver)