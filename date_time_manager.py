import datetime

class DateTimeManager():
    
    @staticmethod
    def get_current_time():
        current_time = datetime.datetime.now()
        current_time_string = current_time.strftime('%I:%M%p')
        return current_time_string
    
    @staticmethod    
    def get_current_date_time():
        current_date_time = datetime.datetime.now()
        current_datetime_string = current_date_time.strftime("%Y_%m_%d_%Hh_%Mm_%Ss")
        return current_datetime_string