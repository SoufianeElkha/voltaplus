
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, 
                           QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from ...config import COLORS
from .new_project import NewProjectDialog

class StartupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Volta+ Preventivi")
        self.project_data = None
        self.action = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)  # Aumenta lo spazio tra gli elementi
        
        # Titolo
        title = QLabel("Benvenuto in Volta+ Preventivi")
        title.setStyleSheet(f"""
            font-size: 20pt;
            font-weight: bold;
            color: {COLORS['primary']};
            margin: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Sottotitolo
        subtitle = QLabel("Scegli un'opzione per iniziare")
        subtitle.setStyleSheet("""
            font-size: 12pt;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Bottoni con stile
        button_style = f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 200px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
                padding: 17px 30px 13px 30px;
            }}
        """
        
        # Bottone Nuovo Progetto
        new_project_btn = QPushButton("Nuovo Progetto")
        new_project_btn.setStyleSheet(button_style)
        new_project_btn.clicked.connect(self.create_new_project)
        layout.addWidget(new_project_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Bottone Apri Progetto
        open_project_btn = QPushButton("Apri Progetto Esistente")
        open_project_btn.setStyleSheet(button_style)
        open_project_btn.clicked.connect(self.open_existing_project)
        layout.addWidget(open_project_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Versione e copyright
        version_label = QLabel("Versione 1.0.0")
        version_label.setStyleSheet("color: gray; margin-top: 20px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Impostazioni finestra
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
            }}
        """)

    def create_new_project(self):
        dialog = NewProjectDialog(self)
        if dialog.exec():
            self.project_data = dialog.get_data()
            self.action = "new"
            self.accept()

    def open_existing_project(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Apri Progetto",
            "",
            "Progetti Volta+ (*.volta);;Tutti i file (*.*)"
        )
        if file_name:
            self.project_data = file_name
            self.action = "open"
            self.accept()
