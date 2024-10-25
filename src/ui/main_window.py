import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QTabWidget, QMessageBox,
                           QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from .dialogs.startup_dialog import StartupDialog
from .dialogs.new_project import NewProjectDialog
from .dialogs.new_tableau import NewTableauDialog
from .widgets.materials_tab import MaterialsTab
from .widgets.labor_widget import LaborWidget
from .widgets.summary_widget import SummaryWidget
from ..models.project import Project, TableauElectrique
from .styles import MAIN_STYLE
from ..config import TAB_COLORS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Mostra dialog iniziale
        startup = StartupDialog()
        if startup.exec():
            if startup.action == "new":
                self.create_new_project(startup.project_data)
            else:
                self.load_existing_project(startup.project_data)
        else:
            sys.exit()
        
        self.setWindowTitle(f"Volta+ Preventivi - {self.project.name}")
        self.setMinimumSize(1600, 900)
        
        self.setup_ui()
        
        # Timer per salvataggio automatico
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(300000)  # 5 minuti
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header con informazioni progetto
        header_layout = QHBoxLayout()
        projet_label = QLabel(f"Progetto: {self.project.name}")
        quadro_label = QLabel(f"Cliente: {self.project.client_name}")
        volta_label = QLabel(f"Volta: {self.project.volta_number}")
        
        header_layout.addWidget(projet_label)
        header_layout.addWidget(quadro_label)
        header_layout.addWidget(volta_label)
        header_layout.addStretch()
        
        # Bottoni
        add_tableau_btn = QPushButton("Aggiungi Quadro")
        save_btn = QPushButton("Salva")
        export_btn = QPushButton("Esporta")
        
        add_tableau_btn.clicked.connect(self.add_new_tableau)
        save_btn.clicked.connect(self.save_project)
        export_btn.clicked.connect(self.export_project)
        
        header_layout.addWidget(add_tableau_btn)
        header_layout.addWidget(save_btn)
        header_layout.addWidget(export_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget per i quadri
        self.tableaux_tabs = QTabWidget()
        self.tableaux_tabs.setTabsClosable(True)
        self.tableaux_tabs.tabCloseRequested.connect(self.close_tableau)
        main_layout.addWidget(self.tableaux_tabs)
        
        # Crea tab per ogni quadro
        for name, tableau in self.project.tableaux.items():
            self.add_tableau_tab(tableau)
        
        # Applica stile
        self.setStyleSheet(MAIN_STYLE)
        
    def create_new_project(self, project_data):
        self.project = Project(
            name=project_data['project_name'],
            client_name=project_data['client_name'],
            volta_number=project_data['volta_number']
        )
        for tableau in project_data['tableaux']:
            self.project.add_tableau(tableau['name'])

    def load_existing_project(self, filename):
        try:
            self.project = Project.load_from_file(filename)
        except Exception as e:
            QMessageBox.critical(self, "Errore",
                            f"Errore durante il caricamento del progetto: {str(e)}")
            sys.exit()


    def add_tableau_tab(self, tableau: TableauElectrique):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Tab per materiali
        materials_tabs = QTabWidget()
        
        # Store the materials_tabs reference in the tab widget
        tab.materials_tabs = materials_tabs
        
        for manufacturer in ['Schneider', 'Hager', 'KNX', 'MCR', 'Swisspro']:
            materials_tab = MaterialsTab(manufacturer)
            # Connetti il segnale dataChanged all'aggiornamento del colore del tab
            materials_tab.dataChanged.connect(self.update_manufacturer_tab_color)
            materials_tabs.addTab(materials_tab, manufacturer)
        
        layout.addWidget(materials_tabs, stretch=2)
        
        # Widget manodopera
        labor_widget = LaborWidget()
        layout.addWidget(labor_widget, stretch=1)
        
        # Widget riepilogo
        summary_widget = SummaryWidget()
        layout.addWidget(summary_widget, stretch=1)
        
        # Aggiungi tab
        self.tableaux_tabs.addTab(tab, tableau.name)
    
    def update_manufacturer_tab_color(self, manufacturer: str, has_content: bool):
        """Aggiorna il colore del tab del manufacturer in base alla presenza di contenuto"""
        current_tab = self.tableaux_tabs.currentWidget()
        if hasattr(current_tab, 'materials_tabs'):
            materials_tabs = current_tab.materials_tabs
            for i in range(materials_tabs.count()):
                if materials_tabs.tabText(i) == manufacturer:
                    color = TAB_COLORS['with_content'] if has_content else TAB_COLORS['default']
                    materials_tabs.tabBar().setTabTextColor(i, QColor(color))
                    break

    def add_new_tableau(self):
        dialog = NewTableauDialog()
        if dialog.exec():
            data = dialog.get_data()
            try:
                tableau = self.project.add_tableau(data['name'])
                self.add_tableau_tab(tableau)
            except ValueError as e:
                QMessageBox.warning(self, "Errore", str(e))
    
    def close_tableau(self, index):
        if self.tableaux_tabs.count() > 1:
            if QMessageBox.question(
                self, "Chiudi Quadro",
                "Sei sicuro di voler chiudere questo quadro?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) == QMessageBox.StandardButton.Yes:
                name = self.tableaux_tabs.tabText(index)
                self.project.remove_tableau(name)
                self.tableaux_tabs.removeTab(index)
        else:
            QMessageBox.warning(self, "Errore",
                              "Non puoi chiudere l'ultimo quadro")
    
    def update_tab_color(self, manufacturer, has_content):
        current_tab = self.tableaux_tabs.currentWidget()
        if hasattr(current_tab, 'materials_tabs'):
            materials_tabs = current_tab.materials_tabs
            for i in range(materials_tabs.count()):
                if materials_tabs.tabText(i) == manufacturer:
                    color = TAB_COLORS['with_content'] if has_content else TAB_COLORS['default']
                    materials_tabs.tabBar().setTabTextColor(i, QColor(color))
                    break
    
    def save_project(self):
        filename = f"{self.project.name}.volta"
        try:
            self.project.save_to_file(filename)
            QMessageBox.information(self, "Salvataggio",
                                  f"Progetto salvato in {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Errore",
                               f"Errore durante il salvataggio: {str(e)}")
    
    def auto_save(self):
        self.save_project()
    
    def export_project(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Preventivo",
            f"Preventivo_{self.project.name}.xlsx",
            "Excel Files (*.xlsx)"
        )
        if filename:
            try:
                self.export_to_excel(filename)
                QMessageBox.information(self, "Export",
                                      f"Preventivo esportato in {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Errore",
                                   f"Errore durante l'esportazione: {str(e)}")
    
    def closeEvent(self, event):
        self.save_project()
        event.accept()

    def setup_visibility_controls(self):
        controls_layout = QHBoxLayout()
        
        # Checkbox per mostrare/nascondere sezioni
        self.labor_checkbox = QCheckBox("Mostra Main d'Œuvre")
        self.labor_checkbox.setChecked(True)
        self.labor_checkbox.stateChanged.connect(self.toggle_labor_visibility)
        
        self.resume_checkbox = QCheckBox("Mostra Résumé")
        self.resume_checkbox.setChecked(True)
        self.resume_checkbox.stateChanged.connect(self.toggle_resume_visibility)
        
        self.tableau_info_checkbox = QCheckBox("Mostra Info Tableau")
        self.tableau_info_checkbox.setChecked(True)
        self.tableau_info_checkbox.stateChanged.connect(self.toggle_tableau_info_visibility)
        
        controls_layout.addWidget(self.labor_checkbox)
        controls_layout.addWidget(self.resume_checkbox)
        controls_layout.addWidget(self.tableau_info_checkbox)
        controls_layout.addStretch()
        
        return controls_layout

    def toggle_labor_visibility(self, state):
        if hasattr(self, 'labor_widget'):
            self.labor_widget.setVisible(state)

    def toggle_resume_visibility(self, state):
        if hasattr(self, 'summary_widget'):
            self.summary_widget.setVisible(state)

    def toggle_tableau_info_visibility(self, state):
        if hasattr(self, 'summary_widget'):
            self.summary_widget.info_group.setVisible(state)
