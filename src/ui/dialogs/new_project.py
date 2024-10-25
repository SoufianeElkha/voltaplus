
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QSpinBox, QFormLayout,
                           QMessageBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from ...config import COLORS, UI_CONFIG

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuovo Progetto")
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Titolo
        title = QLabel("Creazione Nuovo Progetto")
        title.setStyleSheet(f"""
            font-size: 16pt;
            color: {COLORS['primary']};
            font-weight: bold;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Area scrollabile per il form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        form_layout.setSpacing(10)
        
        # Stile per i QLineEdit
        line_edit_style = f"""
            QLineEdit {{
                padding: 8px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['surface']};
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary']};
            }}
        """
        
        # Campi del form
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Nome del progetto")
        self.project_name.setStyleSheet(line_edit_style)
        form_layout.addRow("Nome Progetto:", self.project_name)
        
        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText("Nome del cliente")
        self.client_name.setStyleSheet(line_edit_style)
        form_layout.addRow("Cliente:", self.client_name)
        
        self.volta_number = QLineEdit()
        self.volta_number.setPlaceholderText("Numero Volta")
        self.volta_number.setStyleSheet(line_edit_style)
        form_layout.addRow("Numero Volta:", self.volta_number)
        
        # Numero di quadri
        self.num_tableaux = QSpinBox()
        self.num_tableaux.setMinimum(1)
        self.num_tableaux.setMaximum(10)
        self.num_tableaux.setStyleSheet(f"""
            QSpinBox {{
                padding: 8px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
            }}
        """)
        form_layout.addRow("Numero di Quadri:", self.num_tableaux)
        
        # Container per i quadri
        self.tableaux_container = QVBoxLayout()
        self.update_tableaux_fields(1)
        form_layout.addRow("", self.tableaux_container)
        
        self.num_tableaux.valueChanged.connect(self.update_tableaux_fields)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # Bottoni
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        cancel_button = QPushButton("Annulla")
        ok_button = QPushButton("Crea Progetto")
        
        button_style = f"""
            QPushButton {{
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
        """
        
        cancel_button.setStyleSheet(button_style + f"""
            background-color: {COLORS['background']};
            border: 1px solid {COLORS['border']};
            color: {COLORS['text']};
        """)
        
        ok_button.setStyleSheet(button_style + f"""
            background-color: {COLORS['primary']};
            border: none;
            color: white;
        """)
        
        cancel_button.clicked.connect(self.reject)
        ok_button.clicked.connect(self.validate_and_accept)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(ok_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Dimensioni finestra
        self.setMinimumWidth(500)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
            }}
        """)
    
    def update_tableaux_fields(self, count):
        # Pulisci il container
        while self.tableaux_container.count():
            item = self.tableaux_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Ricrea i campi per ogni quadro
        self.tableau_fields = []
        for i in range(count):
            form = QFormLayout()
            
            name_edit = QLineEdit()
            name_edit.setPlaceholderText(f"Nome del quadro {i+1}")
            name_edit.setStyleSheet(f"""
                QLineEdit {{
                    padding: 8px;
                    border: 1px solid {COLORS['border']};
                    border-radius: 4px;
                }}
                QLineEdit:focus {{
                    border-color: {COLORS['primary']};
                }}
            """)
            
            form.addRow(f"Nome Quadro {i+1}:", name_edit)
            self.tableau_fields.append(name_edit)
            self.tableaux_container.addLayout(form)
    
    def validate_and_accept(self):
        if not self.project_name.text().strip():
            QMessageBox.warning(self, "Errore", "Inserire il nome del progetto")
            return
        
        if not self.client_name.text().strip():
            QMessageBox.warning(self, "Errore", "Inserire il nome del cliente")
            return
            
        if not self.volta_number.text().strip():
            QMessageBox.warning(self, "Errore", "Inserire il numero Volta")
            return
        
        # Verifica che tutti i quadri abbiano un nome
        for i, field in enumerate(self.tableau_fields):
            if not field.text().strip():
                QMessageBox.warning(self, "Errore", f"Inserire il nome per il quadro {i+1}")
                return
        
        self.accept()
    
    def get_data(self):
        return {
            'project_name': self.project_name.text().strip(),
            'client_name': self.client_name.text().strip(),
            'volta_number': self.volta_number.text().strip(),
            'tableaux': [
                {'name': field.text().strip()}
                for field in self.tableau_fields
            ]
        }
