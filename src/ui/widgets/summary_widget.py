from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QLabel, QHeaderView, QDoubleSpinBox,
                           QGroupBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal

from ...config import SUMMARY_SECTIONS, COLORS, APP_CONFIG
from ...utils.error_handler import ErrorHandler

class SummaryWidget(QWidget):
    marginChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Inizializza il margin_spin prima di chiamare setup_ui
        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setRange(0, 100)
        self.margin_spin.setValue(APP_CONFIG['default_margin'])
        self.margin_spin.valueChanged.connect(lambda value: self.marginChanged.emit(value/100))
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)  # Riduce lo spazio tra gli elementi
        
        # Titolo sezione
        title = QLabel("Résumé")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Margine in alto
        margin_layout = QHBoxLayout()
        margin_label = QLabel("Margine Materiale (%):")
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
        costs_layout.setSpacing(0)  # Rimuove lo spazio tra gli elementi
        self.costs_table = QTableWidget()
        self.setup_costs_table()
        costs_layout.addWidget(self.costs_table)
        costs_group.setLayout(costs_layout)
        layout.addWidget(costs_group)
        
        # Sezione Info Tableau
        info_group = QGroupBox("Info Tableau")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)  # Rimuove lo spazio tra gli elementi
        self.info_table = QTableWidget()
        self.setup_info_table()
        info_layout.addWidget(self.info_table)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
    

    def setup_costs_table(self):
        self.costs_table.setColumnCount(2)
        self.costs_table.setRowCount(4)
        self.costs_table.setHorizontalHeaderLabels(["Description", "Valeur"])
        self.costs_table.verticalHeader().setVisible(False)  # Nasconde l'header verticale
        
        # Riduci l'altezza delle righe
        self.costs_table.verticalHeader().setDefaultSectionSize(25)
        
        # Disabilita la griglia
        self.costs_table.setShowGrid(False)
        
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
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.costs_table.setItem(i, 1, value_item)
        
        # Imposta le dimensioni delle colonne
        header = self.costs_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.costs_table.setColumnWidth(1, 100)
        
        # Stile header
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #388E3C;
            }
        """)
        
        # Imposta altezza fissa per la tabella
        total_height = (self.costs_table.horizontalHeader().height() +
                       (self.costs_table.rowHeight(0) * self.costs_table.rowCount()) + 2)
        self.costs_table.setFixedHeight(total_height)
    
    def setup_info_table(self):
        self.info_table.setColumnCount(2)
        self.info_table.setRowCount(len(SUMMARY_SECTIONS['info_tableau']))
        self.info_table.setHorizontalHeaderLabels(["Description", "Valeur"])
        self.info_table.verticalHeader().setVisible(False)  # Nasconde l'header verticale
        
        # Riduci l'altezza delle righe
        self.info_table.verticalHeader().setDefaultSectionSize(25)
        
        # Disabilita la griglia
        self.info_table.setShowGrid(False)
        
        for i, description in enumerate(SUMMARY_SECTIONS['info_tableau']):
            desc_item = QTableWidgetItem(description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.info_table.setItem(i, 0, desc_item)
            
            value_item = QTableWidgetItem("0.00")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.info_table.setItem(i, 1, value_item)
        
        # Imposta le dimensioni delle colonne
        header = self.info_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.info_table.setColumnWidth(1, 100)
        
        # Stile header
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #388E3C;
            }
        """)
    
    def format_number(self, value, decimals=2):
        try:
            num = float(value)
            return f"{num:,.{decimals}f}".replace(",", "'")
        except (ValueError, TypeError):
            return "0.00"
    
    def update_costs(self, material_total, time_total, labor_total):
        margin = self.margin_spin.value() / 100
        material_with_margin = material_total * (1 + margin)
        final_total = material_with_margin + labor_total

        self.costs_table.item(0, 1).setText(self.format_number(material_total))
        self.costs_table.item(1, 1).setText(f"{time_total:.0f} min")
        self.costs_table.item(2, 1).setText(self.format_number(labor_total))
        self.costs_table.item(3, 1).setText(self.format_number(final_total))

        # Evidenzia il totale finale
        final_item = self.costs_table.item(3, 1)
        final_item.setBackground(Qt.GlobalColor.lightGray)
    
    def update_info(self, modules_data):
        for i, key in enumerate(SUMMARY_SECTIONS['info_tableau']):
            value = modules_data.get(key.lower().replace(' ', '_'), 0)
            formatted_value = self.format_number(value) if isinstance(value, float) else str(value)
            
            item = self.info_table.item(i, 1)
            if item:
                item.setText(formatted_value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    
    def get_margin(self):
        return self.margin_spin.value() / 100
    
    def set_margin(self, value):
        self.margin_spin.setValue(value * 100)