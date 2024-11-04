from scraper import StoreForecastScraper
from color_constants import ColorConstants
from date_time_manager import DateTimeManager
from automation_manager import AutomationManager
from selenium.webdriver.support.ui import WebDriverWait
from login_manager import LoginManager

def run_scrape(update_progress, name):
    
    logger = AutomationManager.init_logger()     
    driver = AutomationManager.initialize_driver(logger)
    wait = WebDriverWait(driver, 20)

    current_date_time = DateTimeManager.get_current_date_time()
    output_file_name = f'{name}/store_fore_cast_order_data_{current_date_time}.xlsx'
    writer = AutomationManager.wirter_init(output_file_name)
    update_progress(12)
    login_mgr = LoginManager(driver, wait, logger)
    login_mgr.login()
    update_progress(30)

    scraper = StoreForecastScraper(driver, wait, logger, writer)
    scraper.scrape_store_forecast_data()
    update_progress(66)

    print()
    login_mgr.sign_out()
    print()
    logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Script completed successfully. Exiting ...{ColorConstants.green}')
    print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Script completed successfully. Exiting ...{ColorConstants.green}')
    update_progress(83)
    driver.quit()
    update_progress(100)