import logging
from PyQt6.QtWidgets import QLineEdit, QComboBox, QStyledItemDelegate
from PyQt6.QtCore import Qt

class InlineEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        try:
            if index.column() == 1:  # Reference column
                editor = ReferenceEditor(parent)
                if hasattr(self.parent(), 'reference_completer'):
                    editor.setCompleter(self.parent().reference_completer)
                return editor
            elif index.column() == 0:  # Quantity column
                editor = QuantityEditor(parent)
                return editor
        except Exception as e:
            logging.error(f"Errore nella creazione dell'editor: {str(e)}")
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if value is not None:
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

class ReferenceEditor(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrame(False)  # Rimuove il bordo
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
                padding: 0px 2px;
                font-size: 12px;
            }
            QLineEdit:focus {
                background: white;
                border: 1px solid #4CAF50;
            }
        """)
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.editingFinished.emit()
        super().keyPressEvent(event)

class QuantityEditor(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrame(False)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
                padding: 0px 2px;
                font-size: 12px;
            }
            QLineEdit:focus {
                background: white;
                border: 1px solid #4CAF50;
            }
        """)
        
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.editingFinished.emit()
        super().keyPressEvent(event)


class HoursDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setFrame(False)
        editor.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        editor.setStyleSheet("""
            QLineEdit {
                background: transparent;
                padding: 0px 2px;
                font-size: 12px;
            }
            QLineEdit:focus {
                background: white;
                border: 1px solid #4CAF50;
            }
        """)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(value) if value else "0")

    def setModelData(self, editor, model, index):
        try:
            value = float(editor.text().replace(",", "."))
            model.setData(index, str(value))
        except ValueError:
            model.setData(index, "0")