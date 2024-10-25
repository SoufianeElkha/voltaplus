
import logging
import traceback
from PyQt6.QtWidgets import QMessageBox

class ErrorHandler:
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            filename='volta_plus.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def show_error(parent, title, message, exception=None):
        if exception:
            logging.error(f"{message}: {str(exception)}\n{traceback.format_exc()}")
        
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_warning(parent, title, message):
        logging.warning(message)
        QMessageBox.warning(parent, title, message)
