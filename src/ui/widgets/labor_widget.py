from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QLabel, QHeaderView,
                           QFrame)
from PyQt6.QtCore import Qt, pyqtSignal

from ...config import (LABOR_BASE_RATES, LABOR_COEFFICIENTS, LaborType, 
                      COLORS)
from .custom_editors import HoursDelegate
from ...utils.error_handler import ErrorHandler

class LaborWidget(QWidget):
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_labor_type = LaborType.INTERNAL
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titolo sezione
        title = QLabel("Main d'Œuvre")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Bottoni per il tipo di manodopera
        buttons_layout = QHBoxLayout()
        self.type_buttons = {}
        
        for labor_type in LaborType:
            btn = QPushButton(labor_type.value)
            btn.setProperty("type", "labor")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=labor_type: self.set_labor_type(t))
            buttons_layout.addWidget(btn)
            self.type_buttons[labor_type] = btn
        
        # Seleziona il bottone interno di default
        self.type_buttons[LaborType.INTERNAL].setChecked(True)
        
        layout.addLayout(buttons_layout)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Tabella manodopera
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Aggiorna i colori dei bottoni
        self.update_button_states()
    
    def setup_table(self):
        self.table.setColumnCount(3)
        self.table.setRowCount(len(LABOR_BASE_RATES))
        
        self.table.setHorizontalHeaderLabels(["Type", "Heures", "Tarif"])
        
        # Riduci l'altezza delle righe
        self.table.verticalHeader().setDefaultSectionSize(25)
        
        # Disabilita la griglia
        self.table.setShowGrid(False)
        
        # Popola la tabella
        for i, (labor_type, base_rate) in enumerate(LABOR_BASE_RATES.items()):
            # Tipo (non editabile)
            type_item = QTableWidgetItem(labor_type)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 0, type_item)
            
            # Ore (editabile)
            hours_item = QTableWidgetItem("0")
            hours_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 1, hours_item)
            
            # Tariffa (non editabile)
            coefficient = LABOR_COEFFICIENTS[self.current_labor_type][labor_type]
            rate = base_rate * coefficient
            rate_item = QTableWidgetItem(f"{rate:.2f}")
            rate_item.setFlags(rate_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            rate_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 2, rate_item)
        
        # Imposta le dimensioni delle colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 60)  # Ridotto la larghezza della colonna ore
        self.table.setColumnWidth(2, 80)  # Ridotto la larghezza della colonna tariffa
        
        # Stile header
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #388E3C;
            }
        """)
        
        # Imposta il delegate personalizzato per la colonna delle ore
        self.table.setItemDelegateForColumn(1, HoursDelegate(self))
        
        # Connetti l'evento di modifica
        self.table.itemChanged.connect(self.on_data_changed)
    
    def set_labor_type(self, labor_type: LaborType):
        self.current_labor_type = labor_type
        self.update_rates()
        self.update_button_states()
        self.dataChanged.emit()
    
    def update_rates(self):
        for i, (labor_type, base_rate) in enumerate(LABOR_BASE_RATES.items()):
            coefficient = LABOR_COEFFICIENTS[self.current_labor_type][labor_type]
            rate = base_rate * coefficient
            rate_item = QTableWidgetItem(f"{rate:.2f}")
            rate_item.setFlags(rate_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            rate_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 2, rate_item)
        self.on_data_changed()
    
    def update_button_states(self):
        for labor_type, btn in self.type_buttons.items():
            btn.setChecked(labor_type == self.current_labor_type)
            if labor_type == self.current_labor_type:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1565C0;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
    
    def on_data_changed(self, item=None):
        self.dataChanged.emit()
    
    def get_total_cost(self):
        total_cost = 0
        for row in range(self.table.rowCount()):
            hours_item = self.table.item(row, 1)
            rate_item = self.table.item(row, 2)
            
            if hours_item and rate_item and hours_item.text() and rate_item.text():
                try:
                    hours = float(hours_item.text().replace(",", "."))
                    rate = float(rate_item.text().replace("'", ""))
                    total_cost += hours * rate
                except ValueError:
                    continue
        return total_cost
    
    def get_data(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return {
            'type': self.current_labor_type.value,
            'data': data
        }
    
    def set_data(self, data):
        if 'type' in data:
            for labor_type in LaborType:
                if labor_type.value == data['type']:
                    self.set_labor_type(labor_type)
                    break
        
        if 'data' in data:
            self.table.blockSignals(True)
            for row, row_data in enumerate(data['data']):
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    if col != 1:  # Solo le ore sono editabili
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row, col, item)
            self.table.blockSignals(False)
            self.dataChanged.emit()