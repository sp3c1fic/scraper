import pandas as pd

pd.set_option('mode.chained_assignment', None)

class DataReader:

    @staticmethod 
    def get_last_col_index_from_name(col_name):
        return int(col_name.split('.')[1]) if '.' in col_name else None

    @staticmethod
    def get_product_row_index(inventory_df, product_name):
        return inventory_df.index[inventory_df['Unnamed: 1'] == product_name]

    @staticmethod
    def fill_in_total_values(inventory_df, store_data_df, second_unnamed, col_name, date_index):
        products = ['ah bb kastanjechampignons', 'ah bio kastanjechamp', 'ah bio oesterzwammen', 'ah bio portobello', 'ah bio shiitake',
                    'ah kastanjechampignon', 'ah kastanjechampignons', 'ah kleine kastanjechamp', 'ah witte champignons', 'ah witte champignon']
        delivery_centers = {
            "Hoorn": 1,
            "Overijssel": 2,
            "Pijnacker": 3,
            "Tilburg": 4,
            "Zaandam": 5,
            "Limburg": 6,
        }

        for idx, row in enumerate(second_unnamed):
            if pd.isna(row) or row not in products:
                continue
            try:
                if second_unnamed[idx + 1] == "Nieuwegein":
                    total = DataReader.get_current_total(store_data_df, row, 'Nieuwegein', date_index)
                    inventory_df[col_name][idx + 1] = total
                else:
                    for key, value in delivery_centers.items():
                        total = DataReader.get_current_total(store_data_df, row, key, date_index)
                        inventory_df[col_name][idx + value] = total
            except IndexError:
                pass

    @staticmethod
    def fill_in_last_product(inventory_df, second_unnamed, store_data_df):

        dict_series = second_unnamed.to_dict()
        filtered_dict_series = {k: v for k, v in dict_series.items() if v == 'ah witte champignon'}

        keys = list(filtered_dict_series.keys())
        values = list(filtered_dict_series.values())

        index = keys[0]
        product_name = values[0]
        last_product_df = inventory_df.iloc[index:len(inventory_df) + 1]

        # Iterate through each column
        DataReader.iterate_dataframe_columns(inventory_df, store_data_df, index, product_name)

    @staticmethod
    def iterate_dataframe_columns(inventory_df, store_data_df, index, product_name):

        inventory_df_as_dict = inventory_df.to_dict('list')
        length = len(inventory_df_as_dict['Unnamed: 0'])
        product_number = 535883
        necessary_dates_df = store_data_df.loc[store_data_df['Pr. Num'] == product_number]

        for col in inventory_df:
            date = inventory_df[col][2]  # current column a.k.a expected delivery date

            if date is None:
                continue

            for idx in range(index, length - 1):
                dc = inventory_df["Unnamed: 1"][idx + 1]

                filtered_row = necessary_dates_df.loc[
                    (necessary_dates_df['Store Delivery Date'] == date) &
                    (necessary_dates_df['Pr. Num'] == product_number) &
                    (necessary_dates_df['DC'] == dc)
                    ]

                print(filtered_row)

                if not filtered_row.empty:
                    # Get the first matching index for the specified criteria
                    row_index = filtered_row.index[0]
                    target_total = filtered_row.at[row_index, 'Total']
                    inventory_df[col][idx + 1] = target_total

                    print(
                        f"The row index for {date} with pr number {product_number} and location {dc} is: {row_index}")
                    print(f"The Total value for this row is: {target_total}")
                else:
                    print("No matching row found for the specified criteria.")

    ## TODO WRITE AN ALGORITHM TO FILL IN ALL THE ROWS OF THE LAST PRODUCT A.K.A 'ah witte champignon'

    @staticmethod
    def get_current_product_number(dataframe, index_row):
        return dataframe['Unnamed: 0'][index_row]

    @staticmethod
    def get_current_dc(dataframe, index_row, offset):
        return dataframe['Unnamed: 1'][index_row + offset]


    @staticmethod 
    def is_dc(current_row, dc):
        return current_row == dc

    @staticmethod
    def get_current_total_by_product_number(dataframe, product_name, product_number, date_index):
        return dataframe.loc[
            (dataframe['Pr. Name'] == product_name) & 
            (dataframe['Pr. Num'] == product_number),
            'Total'
        ].iloc[date_index]


    @staticmethod
    def get_current_total_by_date(dataframe, date, index):
        return dataframe.loc[(dataframe['Store Delivery Date'] == date), 'Total'].iloc[index]


    @staticmethod
    def get_current_total(dataframe, product_name, dc, index):
        return dataframe.loc[
            (dataframe['Pr. Name'] == product_name) &
            (dataframe['DC'] == dc),
            'Total'
        ].iloc[index]

    @staticmethod
    def get_current_expected(data_frame, col_name, index_row):
        return data_frame[col_name][index_row + 1]
