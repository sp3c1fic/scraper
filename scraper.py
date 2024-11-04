import pandas as pd

from io import StringIO
from web_constants import WebConstants
from color_constants import ColorConstants
from date_time_manager import DateTimeManager
from web_element_handler import WebElementHandler

# CONSTANT XPATHS OF THE WEB ELEMENTS THE SCRIPT NEEDS TO INTERACT WITH


class StoreForecastScraper:

    def __init__(self, driver, wait, logger, writer):
        self.driver = driver
        self.wait = wait
        self.logger = logger
        self.writer = writer

    #CREATES A SHEET NAME FOR THE WORKSHEET THE EXCEL FILE
    @staticmethod
    def get_sheet_name(sheet_name_element):
        sheet_name_element_text = sheet_name_element.text.split(' ')
        return f'{sheet_name_element_text[4]}_{sheet_name_element_text[5]}'

    #EXTRACTS THE NECESSARY HTML ELEMENTS IN ORDER TO PROPERLY GET THE PRODUCT NUMBER AND NAME

    @staticmethod
    def extract_product_info(product_info_element):
        split_product_info_element = product_info_element.text.split(' ')
        product_number = split_product_info_element[2]
        product_name = ' '.join(split_product_info_element[3:])
        return product_number, product_name

    #EXTRACTS THE NECESSARY HTML ELEMENTS IN ORDER TO PROPERLY GET THE TABLE HEADING AND THE CITY OF DELIVERY

    @staticmethod
    def extract_table_info(table_heading_element):
        city_name = table_heading_element.text.split(' ')[-1]
        return city_name

    @staticmethod
    def process_table_html(table_html):
        html_buffer = StringIO(table_html)
        temp_df = pd.read_html(html_buffer, thousands='.')[0]

        columns_list = list(temp_df.columns)
        columns_list = [col[0] for col in columns_list]
        temp_df.columns = columns_list
        return temp_df

    #INITIALIZES THE DATAFRAME

    @staticmethod
    def define_store_forecast_dataframe(temp_df, product_number, product_name, city_name, columns): 

        temp_df['Pr. Num'] = product_number
        temp_df['Pr. Name'] = product_name
        temp_df['DC'] = city_name       

        temp_df.reset_index(drop=True, inplace=True)

        if all(col in temp_df.columns for col in columns):
            temp_df = temp_df[columns]
        
        return temp_df

    def modify_columns_width(self):
        all_columns_indices = [0, 6, 7, 8]
        col_width = 25

        for sheet_name in self.writer.sheets.keys():
            worksheet = self.writer.sheets[sheet_name]       

            for col_idx in all_columns_indices:
                worksheet.set_column(col_idx, col_idx, col_width)

    def apply_date_format_to_excel(self, workbook):
        
        date_format = workbook.add_format({'num_format': 'dddd dd-mm-yyyy'})
        col_width = 25
        cold_indices = [0]
        for sheet_name in self.writer.sheets.keys():

            worksheet = self.writer.sheets[sheet_name]                
            worksheet.set_column('A:A', col_width)

            for col_idx in cold_indices:
                worksheet.set_column(col_idx, col_idx, cell_format=date_format, width=col_width)

    def apply_numeric_format_to_excel(self, workbook, column_indices_to_convert):
        
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        col_width = 25

        for sheet_name in self.writer.sheets.keys():
            worksheet = self.writer.sheets[sheet_name]

            for col_idx in column_indices_to_convert:
                worksheet.set_column(col_idx, col_idx, cell_format=number_format, width=col_width)

    def process_table(self, table_element, columns, table_index):
        
            current_table_heading_xpath = f'/html/body/div[5]/div/div[3]/div[6]/h1[{table_index + 1}]'
            table_heading_element = WebElementHandler.get_element_by_xpath(self.wait, self.logger, current_table_heading_xpath)
            city_name = self.extract_table_info(table_heading_element)
            product_info_element = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.PRODUCT_INFO_ELEMENT_XPATH)
            product_number, product_name = self.extract_product_info(product_info_element)
            store_forecast_table_html = table_element.get_attribute('outerHTML')

            self.logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Fetching table HTML content for product {product_name} delivered to {city_name} ...{ColorConstants.green}')
            print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Fetching table HTML content for product {product_name} delivered to {city_name} ...{ColorConstants.green}')

            temp_df = self.process_table_html(store_forecast_table_html)
            temp_df = self.define_store_forecast_dataframe(temp_df, product_number, product_name, city_name, columns)

            return temp_df

    def write_dataframe_to_excel(self, table_dataframes, sheet_name): # CHANGE THE SHEET NAME TO SOMETHING MEANINGFUL
        
        if table_dataframes:
            combined_df = pd.concat(table_dataframes, ignore_index=True)
            combined_df.to_excel(self.writer, sheet_name=sheet_name, index=False, engine='xlsxwriter')

    @staticmethod
    def convert_and_format_dataframe(temp_df):
        df_column_names = ['Regular Demand', 'Initial Promotion Demand', 'Total']

        for col_name in df_column_names:
            temp_df[col_name] = temp_df[col_name].astype(int)

            temp_df['Store Delivery Date'] = pd.to_datetime(temp_df['Store Delivery Date'], format='%A %d-%m-%Y', errors='coerce')
            temp_df['Store Delivery Date'] = temp_df['Store Delivery Date'].dt.strftime('%A %d-%m-%Y')

        return temp_df

    #ITERATES THROUGH THE ENTIRE DATAFRAME WITH THE ALREADY FED HTML AND WRITES IT TO AN EXCEL SHEET

    def process_dataframe(self, store_forecast_tables, table_dataframes, sheet_name, columns, temp_df):
        for table_index, table_element in enumerate(store_forecast_tables, start=0):
            temp_df = self.process_table(table_element, columns, table_index)
            table_dataframes.append(temp_df)
            self.convert_and_format_dataframe(temp_df)
        
    def display_fetch_info(self, store_forecast_tables, list_index, sheet_name_element):
            print()
            self.logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] {list_index}: Currently fetched data: {sheet_name_element.text}{ColorConstants.green}')
            print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] {list_index}: Currently fetched data: {sheet_name_element.text}{ColorConstants.green}')
            print()
            self.logger.info(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Fetching {len(store_forecast_tables)} tables ... {ColorConstants.green}')
            print(f'{ColorConstants.green}[{DateTimeManager.get_current_time()}] Fetching {len(store_forecast_tables)} tables ... {ColorConstants.green}')

    def scrape_store_forecast_data(self):

        list_elements = WebElementHandler.get_elements_by_xpath(self.wait, self.logger, WebConstants.LIST_ELEMENTS_XPATH)
        table_dataframes = []
        column_indices_to_convert = [1, 2, 3, 4, 5] #get it somewhere else separately as a constant
        workbook = self.writer.book
        
        for list_index, list_el in enumerate(list_elements, start=1):

            WebElementHandler.click_element_and_wait(list_el)
            store_forecast_btn = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.STORE_FORECAST_BTN_XPATH)
            WebElementHandler.click_element_and_wait(store_forecast_btn)
            sheet_name_element = WebElementHandler.get_element_by_xpath(self.wait, self.logger, WebConstants.TABLE_HEADING_ELEMENT_XPATH)
            sheet_name = self.get_sheet_name(sheet_name_element)  # ultimately this will not exist just must think of a decent sheet name which will be descriptive enough  
            store_forecast_tables = WebElementHandler.get_elements_by_xpath(self.wait, self.logger, WebConstants.STORE_FORECAST_TABLES_XPATH)

            self.display_fetch_info(store_forecast_tables, list_index, sheet_name_element)
            columns = ['Pr. Num', 'Pr. Name', 'DC', 'Store Delivery Date', 'Committed', 'Forecast', 'Committed', 'Forecast']
            temp_df = pd.DataFrame(columns=columns)
            self.process_dataframe(store_forecast_tables, table_dataframes, sheet_name, columns, temp_df)

        self.write_dataframe_to_excel(table_dataframes, sheet_name)
        self.modify_columns_width()    
        self.apply_numeric_format_to_excel(workbook, column_indices_to_convert)
        self.apply_date_format_to_excel(workbook)

        self.writer.close() 


