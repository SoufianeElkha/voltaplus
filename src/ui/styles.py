MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-size: 12px;
}

QTableWidget {
    background-color: white;
    border: 1px solid #ccc;
    gridline-color: #ddd;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QHeaderView::section {
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    border: none;
    border-right: 1px solid #388E3C;
}

QGroupBox {
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 1em;
    padding-top: 1em;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #388E3C;
}

QPushButton[type="labor"] {
    background-color: #2196F3;
}

QPushButton[type="labor"]:hover {
    background-color: #1976D2;
}

QPushButton[type="labor"]:pressed {
    background-color: #1565C0;
}

QPushButton[type="labor"]:checked {
    background-color: #1565C0;
}

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #ccc;
    background-color: white;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    border: 2px solid #4CAF50;
    background-color: #4CAF50;
    border-radius: 3px;
}

QSpinBox, QDoubleSpinBox {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    min-width: 80px;
}

QLineEdit {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

QLineEdit:focus {
    border-color: #4CAF50;
}

QTabWidget::pane {
    border: 1px solid #ccc;
    background: white;
    border-radius: 4px;
}

QTabBar::tab {
    background: #e0e0e0;
    color: #333;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 80px;
}

QTabBar::tab:selected {
    background: #4CAF50;
    color: white;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

QTabBar::tab:hover:!selected {
    background: #eee;
}

QLabel[title="true"] {
    font-size: 14px;
    font-weight: bold;
    color: #333;
    margin: 5px 0;
}

/* Stili per la finestra di dialogo */
QDialog {
    background-color: #f5f5f5;
}

QDialog QLabel {
    color: #333;
}

QDialog QPushButton {
    min-width: 100px;
}

/* Stili per i messaggi di errore */
QMessageBox {
    background-color: #f5f5f5;
}

QMessageBox QPushButton {
    min-width: 100px;
}

/* Stili per il separatore */
QFrame[frameShape="4"] {
    color: #ddd;
    margin: 10px 0;
}
"""

# Stile specifico per i tab con contenuto
TAB_STYLE = {
    'default': """
        QTabBar::tab {
            background-color: #4CAF50;
            color: white;
        }
    """,
    'with_content': """
        QTabBar::tab {
            background-color: #FF5722;
            color: white;
        }
    """
}
