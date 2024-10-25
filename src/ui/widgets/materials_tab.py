import logging
import sqlite3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QCheckBox, QLabel, QHeaderView,
                           QMessageBox, QLineEdit, QCompleter, QStyledItemDelegate,
                           QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from ...config import TAB_COLORS, COLORS, MANUFACTURERS
from ...models import Database
from .custom_editors import InlineEditDelegate
from ...utils.error_handler import ErrorHandler

class MaterialsTab(QWidget):
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None, manufacturer=None, database=None):
        super().__init__(parent)
        self.manufacturer = manufacturer
        self.db = database
        self.has_content = False
        
        # Inizializza il completer qui
        self.setup_reference_autocomplete()
        self.setup_ui()
    
    def setup_reference_autocomplete(self):
        try:
            if hasattr(self.db, 'get_references_by_manufacturer'):
                references = self.db.get_references_by_manufacturer(self.manufacturer)
                self.references_data = {ref: desc for ref, desc in references}
                
                # Crea il completer
                self.reference_completer = QCompleter(list(self.references_data.keys()))
                self.reference_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                self.reference_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            else:
                self.references_data = {}
                self.reference_completer = QCompleter([])
                logging.error("Database non ha il metodo get_references_by_manufacturer")
                
        except Exception as e:
            logging.error(f"Errore nell'inizializzazione dell'autocompletamento: {str(e)}")
            self.references_data = {}
            self.reference_completer = QCompleter([])
        
    def setup_database(self):
        try:
            self.db = sqlite3.connect('volta_plus.db')
            self.setup_reference_autocomplete()
        except Exception as e:
            logging.error(f"Errore nella connessione al database: {str(e)}")
            raise
    
 
    

    
    def setup_table(self):
        self.table.setRowCount(200)
        
        # Colonne base + colonne nascoste
        all_columns = [
            "Quantité", "Référence No.", "Désignation", "Prix", 
            "Temps Article (minutes)", "Prix * Qté", "Temps Article Tot",
            "Numero Module", "Bornes", "1 Borne mm", "Tot mm Bornes",
            "Prix 2S", "Prix 3S"
        ]
        self.table.setColumnCount(len(all_columns))
        self.table.setHorizontalHeaderLabels(all_columns)
        
        # Nascondi le colonne aggiuntive di default
        for col in range(7, len(all_columns)):
            self.table.setColumnHidden(col, True)
        
        # Stile header
        header = self.table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #388E3C;
            }
        """)
        
        # Dimensioni colonne
        self.table.setColumnWidth(0, 80)   # Quantité
        self.table.setColumnWidth(1, 120)  # Référence
        self.table.setColumnWidth(2, 300)  # Désignation
        self.table.setColumnWidth(3, 100)  # Prix
        self.table.setColumnWidth(4, 150)  # Temps Article
        self.table.setColumnWidth(5, 100)  # Prix * Qté
        self.table.setColumnWidth(6, 150)  # Temps Article Tot
        
        # Inizializza le righe
        for row in range(200):
            for col in range(len(all_columns)):
                if col not in [0, 1]:  # Solo Quantité e Référence sono editabili
                    item = QTableWidgetItem("")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row, col, item)
                else:
                    self.table.setItem(row, col, QTableWidgetItem(""))
        
        # Imposta il delegate per l'editing inline
        self.table.setItemDelegate(InlineEditDelegate(self))
        
        # Attiva l'editing al singolo click
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.AnyKeyPressed |
            QAbstractItemView.EditTrigger.DoubleClicked
        )
        
        # Connetti l'evento di modifica cella
        self.table.itemChanged.connect(self.on_cell_changed)
    
    def toggle_column_visibility(self, column_id: str, state: bool):
        column_indices = {
            'num_modules': 7,
            'num_bornes': 8,
            'bornes_mm': 9,
            'tot_bornes_mm': 10,
            'prix_2s': 11,
            'prix_3s': 12
        }
        self.table.setColumnHidden(column_indices[column_id], not state)

    def format_number(self, value, decimals=2):
        try:
            num = float(value)
            return f"{num:,.{decimals}f}".replace(",", "'")
        except (ValueError, TypeError):
            return value

    
    def check_content(self):
        for row in range(self.table.rowCount()):
            qty_item = self.table.item(row, 0)
            ref_item = self.table.item(row, 1)
            if qty_item and ref_item and qty_item.text() and ref_item.text():
                return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            current_row = self.table.currentRow()
            if current_row >= 0:
                reply = QMessageBox.question(
                    self,
                    'Conferma cancellazione',
                    'Sei sicuro di voler cancellare questa riga?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.clear_row(current_row)
        elif event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:  # Copy
                self.copy_row()
            elif event.key() == Qt.Key.Key_V:  # Paste
                self.paste_row()
        super().keyPressEvent(event)

    def clear_row(self, row):
        self.table.blockSignals(True)
        for col in range(self.table.columnCount()):
            self.table.setItem(row, col, QTableWidgetItem(""))
        self.table.blockSignals(False)
        has_content = self.check_content()
        if has_content != self.has_content:
            self.has_content = has_content
            self.dataChanged.emit(self.manufacturer, has_content)

    def copy_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.clipboard_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(current_row, col)
                self.clipboard_data.append(item.text() if item else "")

    def paste_row(self):
        if hasattr(self, 'clipboard_data'):
            current_row = self.table.currentRow()
            if current_row >= 0:
                self.table.blockSignals(True)
                for col, value in enumerate(self.clipboard_data):
                    self.table.setItem(current_row, col, QTableWidgetItem(value))
                self.table.blockSignals(False)
                self.on_cell_changed(self.table.item(current_row, 0))
    
    def save_column_layout(self):
        layout = {}
        for col_id, checkbox in self.column_checkboxes.items():
            layout[col_id] = checkbox.isChecked()
        return layout

    def load_column_layout(self, layout):
        if layout:
            for col_id, is_visible in layout.items():
                if col_id in self.column_checkboxes:
                    self.column_checkboxes[col_id].setChecked(is_visible)
                    self.toggle_column_visibility(col_id, is_visible)
                    
                    
                
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Controlli colonne
        columns_layout = QHBoxLayout()
        columns_label = QLabel("Colonne visibili:")
        columns_layout.addWidget(columns_label)
        
        # Checkbox per ogni colonna aggiuntiva
        self.column_checkboxes = {}
        column_names = {
            'num_modules': 'Numero Module',
            'num_bornes': 'Bornes',
            'bornes_mm': '1 Borne mm',
            'tot_bornes_mm': 'Tot mm Bornes',
            'prix_2s': 'Prix 2S',
            'prix_3s': 'Prix 3S'
        }
        
        for col_id, col_name in column_names.items():
            cb = QCheckBox(col_name)
            cb.setChecked(False)
            cb.stateChanged.connect(
                lambda state, c=col_id: self.toggle_column_visibility(c, state)
            )
            columns_layout.addWidget(cb)
            self.column_checkboxes[col_id] = cb
        
        layout.addLayout(columns_layout)
        
        # Tabella materiali
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
    


    def on_cell_changed(self, item):
        row = item.row()
        col = item.column()
        
        try:
            if col == 1:  # Reference column
                reference = item.text().strip()
                if reference:
                    product = self.db.get_product(reference, self.manufacturer)
                    if product:
                        # Blocca i segnali solo per l'aggiornamento dei dati
                        self.table.blockSignals(True)
                        
                        # Aggiorna i campi
                        self.table.setItem(row, 2, QTableWidgetItem(str(product['designation'])))
                        self.table.setItem(row, 3, QTableWidgetItem(self.format_number(product['price'])))
                        self.table.setItem(row, 4, QTableWidgetItem(str(product['time'])))
                        
                        # Aggiorna campi nascosti
                        self.table.setItem(row, 7, QTableWidgetItem(str(product.get('num_modules', ''))))
                        self.table.setItem(row, 8, QTableWidgetItem(str(product.get('num_bornes', ''))))
                        self.table.setItem(row, 9, QTableWidgetItem(str(product.get('bornes_mm', ''))))
                        self.table.setItem(row, 10, QTableWidgetItem(str(product.get('tot_bornes_mm', ''))))
                        self.table.setItem(row, 11, QTableWidgetItem(self.format_number(product.get('prix_2s', 0))))
                        self.table.setItem(row, 12, QTableWidgetItem(self.format_number(product.get('prix_3s', 0))))
                        
                        # Se c'è già una quantità, aggiorna i totali
                        qty_item = self.table.item(row, 0)
                        if qty_item and qty_item.text():
                            try:
                                qty = float(qty_item.text())
                                self.table.setItem(row, 5, QTableWidgetItem(self.format_number(product['price'] * qty)))
                                self.table.setItem(row, 6, QTableWidgetItem(str(int(product['time'] * qty))))
                            except ValueError:
                                pass
                        
                        self.table.blockSignals(False)
            
            elif col == 0:  # Quantity column
                qty_text = item.text().strip()
                price_item = self.table.item(row, 3)
                time_item = self.table.item(row, 4)
                
                if qty_text and price_item and time_item:
                    try:
                        qty = float(qty_text)
                        price = float(price_item.text().replace("'", ""))
                        time = float(time_item.text())
                        
                        self.table.blockSignals(True)
                        self.table.setItem(row, 5, QTableWidgetItem(self.format_number(price * qty)))
                        self.table.setItem(row, 6, QTableWidgetItem(str(int(time * qty))))
                        self.table.blockSignals(False)
                    except ValueError:
                        pass
            
            # Verifica se c'è contenuto nella tabella
            has_content = self.check_content()
            if has_content != self.has_content:
                self.has_content = has_content
                self.dataChanged.emit()
            
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento della riga: {str(e)}")
