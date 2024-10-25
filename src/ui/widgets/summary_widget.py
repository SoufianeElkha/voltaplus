
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QLabel, QHeaderView, QDoubleSpinBox,
                           QGroupBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from src.config import SUMMARY_SECTIONS

class SummaryWidget(QWidget):
    marginChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titolo sezione
        title = QLabel("Résumé")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Margine in alto
        margin_layout = QHBoxLayout()
        margin_label = QLabel("Margine Materiale (%):")
        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setRange(0, 100)
        self.margin_spin.setValue(25)
        self.margin_spin.valueChanged.connect(self.marginChanged.emit)
        margin_layout.addWidget(margin_label)
        margin_layout.addWidget(self.margin_spin)
        margin_layout.addStretch()
        layout.addLayout(margin_layout)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Sezione Costi
        costs_group = QGroupBox("Costi")
        costs_layout = QVBoxLayout()
        self.costs_table = QTableWidget()
        self.setup_costs_table()
        costs_layout.addWidget(self.costs_table)
        costs_group.setLayout(costs_layout)
        layout.addWidget(costs_group)
        
        # Sezione Info Tableau
        info_group = QGroupBox("Info Tableau")
        info_layout = QVBoxLayout()
        self.info_table = QTableWidget()
        self.setup_info_table()
        info_layout.addWidget(self.info_table)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
    
    def setup_costs_table(self):
        self.costs_table.setColumnCount(2)
        self.costs_table.setRowCount(4)  # Solo 4 righe per i costi
        self.costs_table.setHorizontalHeaderLabels(["Description", "Valeur"])
        
        # Riduci l'altezza delle righe
        self.costs_table.verticalHeader().setDefaultSectionSize(25)
        
        # Imposta le righe dei costi
        cost_rows = [
            "Total Matériel",
            "Total Temps",
            "Total Main d'Œuvre",
            "Total Final"
        ]
        
        for i, description in enumerate(cost_rows):
            desc_item = QTableWidgetItem(description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.costs_table.setItem(i, 0, desc_item)
            
            value_item = QTableWidgetItem("0.00")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.costs_table.setItem(i, 1, value_item)
        
        # Imposta le dimensioni delle colonne
        header = self.costs_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.costs_table.setColumnWidth(1, 120)  # Ridotto la larghezza della colonna valori

    
    def setup_info_table(self):
        self.info_table.setColumnCount(2)
        self.info_table.setRowCount(len(SUMMARY_SECTIONS['info_tableau']))
        self.info_table.setHorizontalHeaderLabels(["Description", "Valeur"])
        
        # Stile header
        header = self.info_table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #388E3C;
            }
        """)
        
        for i, description in enumerate(SUMMARY_SECTIONS['info_tableau']):
            # Descrizione (non editabile)
            desc_item = QTableWidgetItem(description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.info_table.setItem(i, 0, desc_item)
            
            # Valore (non editabile)
            value_item = QTableWidgetItem("0.00")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.info_table.setItem(i, 1, value_item)
        
        # Dimensioni colonne
        header = self.info_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.info_table.setColumnWidth(1, 150)
    
    def update_costs(self, costs_data):
        for i, (value) in enumerate(costs_data):
            self.costs_table.setItem(i, 1, QTableWidgetItem(str(value)))
    
    def update_info(self, info_data):
        for i, (value) in enumerate(info_data):
            self.info_table.setItem(i, 1, QTableWidgetItem(str(value)))
    
    def get_margin(self):
        return self.margin_spin.value() / 100
    
    def set_margin(self, value):
        self.margin_spin.setValue(value * 100)

    def calculate_additional_stats(self):
        total_modules = float(self.info_table.item(10, 1).text() or 0)
        total_bornes = float(self.info_table.item(11, 1).text() or 0)
        
        # Calcola statistiche aggiuntive
        stats = {
            'Moduli per metro': f"{total_modules / 0.8:.1f}" if total_modules > 0 else "0",
            'Media bornes per modulo': f"{total_bornes / total_modules:.1f}" if total_modules > 0 else "0",
            'Occupazione stimata (%)': f"{(total_modules * 1.3 / 80) * 100:.1f}%" if total_modules > 0 else "0%"
        }
        
        # Aggiorna la tabella delle statistiche
        for i, (key, value) in enumerate(stats.items()):
            if self.info_table.rowCount() < len(stats) + 10:
                self.info_table.insertRow(self.info_table.rowCount())
            self.info_table.setItem(i + 10, 0, QTableWidgetItem(key))
            self.info_table.setItem(i + 10, 1, QTableWidgetItem(value))
