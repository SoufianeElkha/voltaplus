
import sys
import os
import logging
from PyQt6.QtWidgets import QApplication

# Aggiungi il percorso del progetto al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.ui.main_window import MainWindow

def main():
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Errore critico nell'applicazione: {str(e)}")
        raise

if __name__ == '__main__':
    main()
