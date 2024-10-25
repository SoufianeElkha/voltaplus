from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, 
                           QFileDialog, QLabel)
from PyQt6.QtCore import Qt
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
        
        # Titolo
        title = QLabel("Benvenuto in Volta+ Preventivi")
        title.setStyleSheet("font-size: 16pt; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Bottoni
        new_project_btn = QPushButton("Nuovo Progetto")
        open_project_btn = QPushButton("Apri Progetto Esistente")
        
        new_project_btn.clicked.connect(self.create_new_project)
        open_project_btn.clicked.connect(self.open_existing_project)
        
        new_project_btn.setMinimumHeight(40)
        open_project_btn.setMinimumHeight(40)
        
        layout.addWidget(new_project_btn)
        layout.addWidget(open_project_btn)
        
        self.setMinimumWidth(300)

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
