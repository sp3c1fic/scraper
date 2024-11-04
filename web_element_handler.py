import sys
import time

from color_constants import ColorConstants
from selenium.webdriver.common.by import By
from date_time_manager import DateTimeManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class WebElementHandler:

    @staticmethod
    def get_element_by_xpath(wait, logger, xpath):
        try:
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except NoSuchElementException:
            logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error: No such web element found for XPath: {xpath}. Please check the XPath or contact the developer.{ColorConstants.red}')
            logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Terminating script... {ColorConstants.green}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error: No such web element found for XPath: {xpath}. Please check the XPath or contact the developer.{ColorConstants.red}')
            print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Terminating script... {ColorConstants.green}')
            sys.exit(0)

    @staticmethod
    def get_elements_by_xpath(wait, logger, xpath):
        try:
            return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except NoSuchElementException:
            logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error: No such web element found for XPath: {xpath}. Please check the XPath or contact the developer.{ColorConstants.red}')
            logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Terminating script... {ColorConstants.green}')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error: No such web element found for XPath: {xpath}. Please check the XPath or contact the developer.{ColorConstants.red}')
            print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Terminating script... {ColorConstants.green}')
            sys.exit(0)

    @staticmethod
    def click_element_and_wait(element, wait_time=3):   
        try:    
            element.click()
            time.sleep(wait_time)
        except ElementClickInterceptedException:
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Element click intercepted. Please restart the script.{ColorConstants.red}')
            sys.exit(0)