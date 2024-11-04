
import re
import sys

from color_constants import ColorConstants
class LoginValidator:

    @staticmethod
    def validate_credentials(login_email, login_password):
        return not login_email or not login_password

    @staticmethod
    def validate_email_format(email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return not re.match(email_pattern, email)

    @staticmethod
    def validate_url_format(url):
        url_pattern = r'^https?://[\w.-]+(\.[\w.-]+)+[/#?]?.*$'
        return re.match(url_pattern, url)
        
    @staticmethod
    def is_url_valid(self, url):
    
        if url and self.validate_url_format(url):
            print(f'{ColorConstants.green}[+] URL has been successfully loaded.{ColorConstants.green}')
        else:
            print(f'[!] Please provide an url in a valid format inside of the config.json file and restart the script')
            print(f'[!] Terminating script')
            sys.exit(0)
            
