from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QSpinBox, QFormLayout,
                           QMessageBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuovo Progetto")
        self.setModal(True)
        self.tableaux_widgets = []  # Per tenere traccia dei widget dei quadri
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Form layout per i campi principali
        form_layout = QFormLayout()
        
        # Nome progetto
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Inserire nome progetto")
        form_layout.addRow("Nome Progetto:", self.project_name)
        
        # Cliente
        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText("Inserire nome cliente")
        form_layout.addRow("Cliente:", self.client_name)

        # Numero Volta (unico per progetto)
        self.volta_number = QLineEdit()
        self.volta_number.setPlaceholderText("Inserire numero Volta")
        form_layout.addRow("Numero Volta:", self.volta_number)
        
        # Numero di quadri
        self.num_tableaux = QSpinBox()
        self.num_tableaux.setMinimum(1)
        self.num_tableaux.setMaximum(50)
        form_layout.addRow("Numero di Quadri:", self.num_tableaux)
        
        main_layout.addLayout(form_layout)
        
        # ScrollArea per i quadri
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_content = QWidget()
        self.tableaux_layout = QVBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        
        main_layout.addWidget(scroll)
        
        # Bottoni
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annulla")
        
        ok_button.clicked.connect(self.validate_and_accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)
        
        # Connetti il cambio di numero quadri
        self.num_tableaux.valueChanged.connect(self.update_tableaux_fields)
        
        # Inizializza il primo quadro
        self.update_tableaux_fields(1)
        
    def clear_tableaux_layout(self):
        # Rimuovi tutti i widget esistenti
        self.tableaux_widgets.clear()
        while self.tableaux_layout.count():
            item = self.tableaux_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def update_tableaux_fields(self, count):
        self.clear_tableaux_layout()
        
        # Crea i nuovi campi
        for i in range(count):
            form = QFormLayout()
            name_edit = QLineEdit()
            name_edit.setPlaceholderText(f"Nome Quadro {i+1}")
            form.addRow(f"Nome Quadro {i+1}:", name_edit)
            
            # Aggiungi il widget al layout e alla lista
            widget = QWidget()
            widget.setLayout(form)
            self.tableaux_layout.addWidget(widget)
            self.tableaux_widgets.append(name_edit)
    
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
        for name_edit in self.tableaux_widgets:
            if not name_edit.text().strip():
                QMessageBox.warning(self, "Errore", "Inserire il nome per tutti i quadri")
                return
        
        self.accept()
    
    def get_data(self):
        return {
            'project_name': self.project_name.text().strip(),
            'client_name': self.client_name.text().strip(),
            'volta_number': self.volta_number.text().strip(),
            'tableaux': [
                {'name': name_edit.text().strip()}
                for name_edit in self.tableaux_widgets
            ]
        }