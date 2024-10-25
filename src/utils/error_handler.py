
import logging
import traceback
from PyQt6.QtWidgets import QMessageBox

class ErrorHandler:
    @staticmethod
    def show_error(parent, title, message, exception=None):
        if exception:
            logging.error(f"{message}: {str(exception)}\n{traceback.format_exc()}")
            QMessageBox.critical(parent, title, f"{message}\n\nDettagli: {str(exception)}")
        else:
            logging.error(message)
            QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_warning(parent, title, message):
        logging.warning(message)
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_info(parent, title, message, show_dialog=True):
        logging.info(message)
        if show_dialog:
            QMessageBox.information(parent, title, message)
