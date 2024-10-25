
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt

class NewTableauDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuovo Quadro Elettrico")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Nome quadro
        self.tableau_name = QLineEdit()
        self.tableau_name.setPlaceholderText("Inserire nome quadro")
        form_layout.addRow("Nome Quadro:", self.tableau_name)
        
        layout.addLayout(form_layout)
        
        # Bottoni
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annulla")
        
        ok_button.clicked.connect(self.validate_and_accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
    
    def validate_and_accept(self):
        if not self.tableau_name.text().strip():
            QMessageBox.warning(self, "Errore", "Inserire il nome del quadro")
            return
        
        self.accept()
    
    def get_data(self):
        return {
            'name': self.tableau_name.text().strip()
        }
