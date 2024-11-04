import sys
from main import run_scrape

from test import iterate_dataframes ## Rename the file and the function
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QThread, QDir, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, 
    QLineEdit, QPushButton, QWidget, QLabel, QComboBox, QMessageBox, QProgressBar, QFileDialog,
)

# TODO ICONS must be moved to the app's directory. Their absolute path should not be used.
# TODO ICONS CURRENTLY DELETED

class TransferThread(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, task_name, name):
        super().__init__()
        self.task_name = task_name
        self.name = name
        self.is_active = True
        self.output_dir = ""

    def run(self):
        iterate_dataframes(self.update_progress.emit, self.name, self.output_dir)

    def stop(self):
        self.is_active = False

class ScrapeThread(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, task_name, name):
        super().__init__()
        self.task_name = task_name
        self.name = name
        self.is_active = True
        self.output_dir = ""

    def run(self): 
        self.is_active = True
        run_scrape(self.update_progress.emit, self.name)

    def stop(self):
        self.is_active = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scraper 0.1")
        self.setWindowIcon(QIcon("C:\\Users\\stjimmyyy\\Downloads\\Scraper-icon_icon-icons.com_52532")) ## fix this
        self.setFixedSize(QSize(420, 400))

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        main_layout = QVBoxLayout()

        # Vertical layout for the label and input/button
        directory_layout = QVBoxLayout()

        # Label for output directory
        label = QLabel("Uitvoermap:", self)
        directory_layout.addWidget(label)

        # Horizontal layout for QLineEdit and button

        input_button_layout = QHBoxLayout()

        # QLineEdit for output directory
        self.input = QLineEdit(self)
        self.input.setReadOnly(True)
        self.input.setFixedWidth(250)
        self.input.setPlaceholderText("Selecteer uitvoermap")
        input_button_layout.addWidget(self.input)

        # Button for selecting output directory
        self.select_button = QPushButton("Selecteer", self)
        self.select_button.setIcon(QIcon('C:\\Users\\stjimmyyy\\Downloads\\floppy-disk')) ## fix this
        self.select_button.clicked.connect(self.pick_save_directory)
        self.select_button.setIconSize(QSize(16, 16))
        input_button_layout.addWidget(self.select_button)

        # Add horizontal layout to directory layout
        directory_layout.addLayout(input_button_layout)

        # Add the directory layout to the main layout
        main_layout.addLayout(directory_layout)

        # Label for scraped data file
        scraped_data_file_label = QLabel("Geschraapt gegevensbestand:", self)
        main_layout.addWidget(scraped_data_file_label)

        # Horizontal layout for scraped data file input and button
        scraped_data_button_layout = QHBoxLayout()

        # QLineEdit for scraped data file
        self.scraped_data_file_input = QLineEdit(self)
        self.scraped_data_file_input.setReadOnly(True)
        self.scraped_data_file_input.setFixedWidth(250)
        self.scraped_data_file_input.setPlaceholderText("Selecteer geschraapt gegevensbestand")
        scraped_data_button_layout.addWidget(self.scraped_data_file_input)

        # Button for selecting scraped data file
        self.scraped_data_select_button = QPushButton("Selecteer", self)
        self.scraped_data_select_button.setIcon(QIcon('C:\\Users\\stjimmyyy\\Downloads\\loupe')) ## fix this
        self.scraped_data_select_button.clicked.connect(self.pick_scraped_file)
        self.scraped_data_select_button.setIconSize(QSize(16, 16))
        scraped_data_button_layout.addWidget(self.scraped_data_select_button)

        # Add the scraped data file layout
        main_layout.addLayout(scraped_data_button_layout)

        # # Dropdown for selecting time range
        # time_range_layout = QVBoxLayout()
        # time_range_label = QLabel("Select Time Range:", self)
        # time_range_layout.addWidget(time_range_label)

        # self.time_range_combo = QComboBox(self)
        # self.time_range_combo.addItems(["None", "10 minutes", "30 minutes", "45 minutes", "1 hour", "2 hours"])
        # time_range_layout.addWidget(self.time_range_combo)

        # main_layout.addLayout(time_range_layout)

        # Scrape button
        self.scrape_button = QPushButton("Schrapen", self)
        self.scrape_button.setFixedWidth(100)
        self.scrape_button.setIcon(QIcon("C:\\Users\\stjimmyyy\\Downloads\\web-crawler")) ## fix this
        self.scrape_button.clicked.connect(self.start_scraping)

        self.transfer_button = QPushButton("Overdracht", self)
        self.transfer_button.setFixedWidth(100)
        self.transfer_button.setIcon(QIcon("C:\\Users\\stjimmyyy\\Downloads\\transfer")) ## fix this
        self.transfer_button.clicked.connect(self.start_transfer)

        
        close_button_layout = QHBoxLayout()
        self.close_button = QPushButton("Sluiten", self)
        self.close_button.setFixedWidth(100)
        self.close_button.setIcon(QIcon("C:\\Users\\stjimmyyy\\Downloads\\close")) ## fix this
        self.close_button.clicked.connect(self.exit_program)

        close_button_layout.addWidget(self.close_button)

        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.scrape_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.transfer_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Set the main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_transfer(self):

        if self.scraped_data_file_input.text() is None or self.scraped_data_file_input.text() == '':
            QMessageBox.warning(self, "Bestand niet gevonden!", "Kon het bestand 'geschraapte gegevens' niet vinden!")
            return

        self.disable_ui()
        self.operation = "Transfer"
        self.transfer_thread = TransferThread(self.operation, self.scraped_data_file_input.text())
        self.transfer_thread.output_dir = self.input.text()
        self.transfer_thread.update_progress.connect(self.update_transfer_progress)
        self.transfer_thread.finished.connect(self.cleanup_transfer_thread)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.transfer_thread.start()


    def start_scraping(self):
        self.disable_ui()
        self.operation = "Scrape"
        self.scrape_thread = ScrapeThread(self.operation, self.input.text())
        self.scrape_thread.output_dir = self.input.text()
        self.scrape_thread.update_progress.connect(self.update_scrape_progress)
        self.scrape_thread.finished.connect(self.cleanup_scrape_thread)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.scrape_thread.start()

    def disable_ui(self):
    # Disable buttons and inputs
        self.scraped_data_file_input.setDisabled(True)
        self.input.setDisabled(True)
        self.scrape_button.setDisabled(True)
        self.transfer_button.setDisabled(True)
        self.select_button.setDisabled(True)
        # self.time_range_combo.setDisabled(True)
        self.scraped_data_select_button.setDisabled(True)
        self.close_button.setDisabled(True)

    def enable_ui(self):
        # Enable buttons and inputs
        self.scraped_data_file_input.setDisabled(False)
        self.input.setDisabled(False)
        self.scrape_button.setDisabled(False)
        self.transfer_button.setDisabled(False)
        self.select_button.setDisabled(False)
        #self.time_range_combo.setDisabled(False)
        self.scraped_data_select_button.setDisabled(False)
        self.close_button.setDisabled(False)

    def cleanup_transfer_thread(self):
        self.transfer_thread = None
        self.enable_ui()
        self.progress_bar.hide()

    def cleanup_scrape_thread(self):
        self.scrape_thread = None
        self.enable_ui()
        self.progress_bar.hide()

    def update_transfer_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "Overdracht voltooid", "Overdracht van 'Totaal'-gegevens is succesvol verlopen!")

    def update_scrape_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "Schrapen voltooid", "Schrapen succesvol voltooid!") # messages can be turned into constants to avoid hardcoding

    def pick_save_directory(self):
        dialog = QFileDialog()
        save_dir_path = dialog.getExistingDirectory(None, "Select folder")

        if save_dir_path == "" or save_dir_path == None:
            self.input.setText("")
            return ""

        self.input.setText(save_dir_path)
        return save_dir_path
    
    def pick_scraped_file(self):
        dialog = QFileDialog()
        file_path, _ = dialog.getOpenFileName(
            self,
            "Open file",
            QDir.homePath(),
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path == "" or file_path == None:
            self.input.setText("")
            return ""

        if "store_fore_cast" not in file_path:
            QMessageBox.critical(self, "Ongeldig bestand", "Het formaat van het geselecteerde bestand is niet geldig!")
            return

        self.scraped_data_file_input.setText(file_path)
        return file_path
    
    def exit_program(self):
        try:
            # Check and stop the scrape_thread if it exists and is running
            if hasattr(self, 'scrape_thread') and self.scrape_thread.isRunning():
                self.scrape_thread.stop()  # Stop the thread properly
                self.scrape_thread.quit()  # Ensure the thread is quit
                self.scrape_thread.wait()  # Wait for the thread to terminate

            # Check and stop the transfer_thread if it exists and is running
            if hasattr(self, 'transfer_thread') and self.transfer_thread.isRunning():
                self.transfer_thread.stop()  # Stop the thread properly
                self.transfer_thread.quit()  # Ensure the thread is quit
                self.transfer_thread.wait()  # Wait for the thread to terminate

        except Exception as e:
            print(f"Exception occurred: {e}")
            app.quit()  # Immediately quit the app if any exception occurs

        # After successfully quitting threads, exit the app
        app.quit()  # Quit the app gracefully after stopping all threads

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
