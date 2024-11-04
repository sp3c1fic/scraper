
import sys
import logging
import warnings
import pandas as pd

from selenium import webdriver
from date_time_manager import DateTimeManager
from selenium.webdriver import FirefoxOptions
from color_constants import ColorConstants
from selenium.webdriver.firefox.service import Service as FirefoxService

#TODO must implement Chrome driver functionality as well

class AutomationManager:

    @staticmethod
    def init_logger():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log_file')
        logger = logging.getLogger()
        return logger
    @staticmethod
    def wirter_init(output_file_name):
        return pd.ExcelWriter(output_file_name, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}}, date_format='dddd dd-mm-yyyy')
    @staticmethod
    def initialize_driver(logger):

    #Ignoring the deprecation warnings since we currently have no other options for setting up the log output
        try:
            warnings.simplefilter('ignore', category=DeprecationWarning)
            gecko_driver_path = r'C:\Users\stjimmyyy\Downloads\scraper\scraper\geckodriver.exe' # move to the config.json file
            opts = FirefoxOptions()
            opts.add_argument('--headless')
            firefox_service = FirefoxService(executable_path=gecko_driver_path, log_output=None)
            driver = webdriver.Firefox(service=firefox_service, options=opts)
            return driver
        except Exception:
            logger.error(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error occured while trying to initialize driver. Please restart the script.')
            print(f'{ColorConstants.red}[{DateTimeManager.get_current_time()}] Error occured while trying to initialize driver. Please restart the script.')
            sys.exit(0)
