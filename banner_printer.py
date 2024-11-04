import pandas as pd

from web_constants import WebConstants
from color_constants import ColorConstants
from date_time_manager import DateTimeManager

class BannerPrinter():

    @staticmethod
    def print_banner():
        print()
        print(f"""{ColorConstants.green}

            ╔════════════════════════════════════════════════════════╗
            ║███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ ║
            ║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗║
            ║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝║
            ║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗║
            ║███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║║
            ║╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝║
            ╚════════════════════════════════════════════════════════╝

        {ColorConstants.green}""")
        print()
        print()
        print(f'{ColorConstants.red}WEB SCRAPING SCRIPT BY stjimmyyy v 0.1 (beta){ColorConstants.red}. Script started at: {DateTimeManager.get_current_time()}')
        print()
        print()
        print(f'Pandas current version: {pd.__version__}')
        print()
