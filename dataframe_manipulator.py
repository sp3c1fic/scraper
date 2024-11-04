import datetime
from reader import DataReader

class DataFrameManipulator:
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    
    def reassign_data(self, first_dataframe, second_dataframe):
        count = 0
        date = None

        store_data_dict = {
            'Store Delivery Date': [],
            'Product Name': [],
            'DC': [],
            'Total': []
        }

        for index, row in first_dataframe.iterrows():
            date_format = '%d-%m-%Y'
            date_str = row['Store Delivery Date'].split(' ')[1]
            date = datetime.datetime.strptime(date_str, date_format)
            product_name = row['Pr. Name']
            total = row['Total']
            dc = row['DC']
            

            store_data_dict['Store Delivery Date'].append(date)
            store_data_dict['Product Name'].append(product_name)
            store_data_dict['DC'].append(dc)
            store_data_dict['Total'].append(total)

        

            count += 1
            print(f'#{count}: Product name - {product_name} - Store Delivery Date - {date} - DC {dc} - Total {total} - Type of total {type(total)}')


        print(f'Total number of date rows: {count}')

        #print(store_data_dict)



    def split_dataframe(self):
        selected_cols = ['Store Delivery Date', 'Total', 'Pr. Name', 'DC']
        split_df = self.dataframe[selected_cols].reset_index(drop=True)

        print()
        print(f'Split Dataframe: \n')
        print(split_df)


        print()

