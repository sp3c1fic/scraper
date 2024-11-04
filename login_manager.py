import sys
import time
import json
import getpass

from web_constants import WebConstants
from color_constants import ColorConstants
from login_validator import LoginValidator
from date_time_manager import DateTimeManager
from web_element_handler import WebElementHandler

class LoginManager:

    def __init__(self, driver, wait, logger):
        self.driver = driver
        self.wait = wait
        self.logger = logger
        self.file_path = 'config.json'

    @staticmethod
    def is_max_attempt_reached(current_attempt, max_attempt):
        return current_attempt == max_attempt

    @staticmethod
    def get_credentials_input():
        login_email = input(f'{ColorConstants.yellow}[{DateTimeManager.get_current_time()}] Enter user email to sign in: {ColorConstants.yellow}')
        print()
        login_password = getpass.getpass(f'{ColorConstants.yellow}[{DateTimeManager.get_current_time()}] Enter user password: {ColorConstants.yellow}')
        print()
        return login_email, login_password

    def handle_login_input(self, login_email, login_password):
        if  LoginValidator.validate_credentials(login_email, login_password):
            self.logger.warning(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Email and password cannot be empty! Please provide both.{ColorConstants.red}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Email and password cannot be empty! Please provide both.{ColorConstants.red}')
            print()
            return False
        elif LoginValidator.validate_email_format(login_email):
            self.logger.warning(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Invalid email format. Please enter a valid email address.{ColorConstants.red}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Invalid email format. Please enter a valid email address.{ColorConstants.red}')
            print()
            return False
        return True

    def load_url(self, file_path):

        try: 
            with open(file_path, 'r') as config_file:
                config = json.load(config_file)
            return config.get('url')    
        except FileNotFoundError as e:
            error_name = e.__class__.__name__
            self.logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] {error_name}: The config file "{file_path}" was not found. Please create the config file with the URL.{ColorConstants.red}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] {error_name}: The config file "{file_path}" was not found. Please create the config file with the URL.{ColorConstants.red}')
            print()
            url = input(f'{ColorConstants.yellow}Enter url manually: {ColorConstants.yellow}')
            LoginValidator.is_url_valid(self, url=url)
            return url
        
    @staticmethod
    def load_credentials(self):
        try: 
            with open(self.file_path, 'r') as config_file:
                config = json.load(config_file)
            return config.get('username'), config.get('password')    
        except Exception:
            raise FileNotFoundError('Config.json not set up properly or does not exist.') 

    def login(self):
        current_attempt = 0
        url = self.load_url(self.file_path)

        while current_attempt < WebConstants.MAX_ATTEMPT:        

            #move the code below to a separate function and add error handling

            self.driver.get(url) # throws an exception

            login_email, login_password = self.load_credentials(self)

            if not self.handle_login_input(login_email, login_password):
                continue  
    
            username_field = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.USERNAME_FIELD_XPATH)
            password_field = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.PASSWORD_FIELD_XPATH)

            username_field.send_keys(login_email)
            password_field.send_keys(login_password)

            login_btn = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.LOGIN_BUTTON_XPATH)
            
            WebElementHandler.click_element_and_wait(login_btn)
            
            print(f'{ColorConstants.yellow}[{DateTimeManager.get_current_time()}] Attempting to login...{ColorConstants.yellow}')
            print()
            # move the code below to a separate function

            try:
                main_menu = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.MAIN_MENU_XPATH)

                if main_menu:
                    print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Login successful{ColorConstants.green}')
                    print()
                    break
            except Exception:
                self.logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error occurred upon login. Please try again. Attempts left {WebConstants.MAX_ATTEMPT - (current_attempt + 1)} out of {WebConstants.MAX_ATTEMPT}{ColorConstants.red}')
                print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error occurred upon login. Please try again. Attempts left {WebConstants.MAX_ATTEMPT - (current_attempt + 1)} out of {WebConstants.MAX_ATTEMPT}{ColorConstants.red}')
                print()
            current_attempt += 1

            if self.is_max_attempt_reached(current_attempt, WebConstants.MAX_ATTEMPT):
                self.logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Max login attempts reached. Terminating script ...{ColorConstants.red}')
                print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Max login attempts reached. Terminating script ...{ColorConstants.red}')
                sys.exit()

    def sign_out(self):
        ul_elements = WebElementHandler.get_elements_by_xpath(self.wait, self.logger, WebConstants.UL_ELEMENTS_XPATH)

        try:
            if ul_elements is None:
                sign_out_btn = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.SIGN_OUT_BTN_XPATH)
                sign_out_btn.click()
                self.logger.info(f'{ColorConstants.yellow}[{DateTimeManager.get_current_time()}] Logging out...{ColorConstants.yellow}')
                print(f'{ColorConstants.yellow}[{DateTimeManager.get_current_time()}] Logging out...{ColorConstants.yellow}')
                print()
                time.sleep(3)
                self.logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] You have successfully logged out {ColorConstants.green}')
                print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] You have successfully logged out {ColorConstants.green}')
                print()
                
        except Exception:
            self.logger.info(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] An error occurred upon logging out... Terminating script... {ColorConstants.red}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] An error occurred upon logging out... Terminating script... {ColorConstants.red}')
            sys.exit(0)