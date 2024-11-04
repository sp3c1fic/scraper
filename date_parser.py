import pandas as pd

class DateParser:

    @staticmethod
    def parse_date(date_str):
        try:
            date_parts = date_str.split()

            if len(date_parts) == 2:
                day_month_year = date_parts[1].split('-')

                if len(day_month_year) == 3:
                    formatted_date = f"{date_parts[0]} {day_month_year[0].zfill(2)}-{day_month_year[1]}-{day_month_year[2]}"
                    return pd.to_datetime(formatted_date, format='%A %d-%m-%Y', errors='raise', dayfirst=True)
        except: 
            raise ValueError(f'Unable to parse dateL: {formatted_date}')
        return pd.NaT