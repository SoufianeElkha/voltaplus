import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Aggiungi il percorso del progetto al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importazioni locali
from src.ui.main_window import MainWindow
from src.config import APP_CONFIG

def setup_logging():
    logging.basicConfig(
        filename=APP_CONFIG['log_file'],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    try:
        # Setup logging
        setup_logging()
        
        # Crea l'applicazione
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Disabilita l'auto scale dei DPI
        app.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
        
        # Crea e mostra la finestra principale
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Errore critico nell'applicazione: {str(e)}")
        raise

if __name__ == '__main__':
    main()