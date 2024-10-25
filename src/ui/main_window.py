import logging
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QTabWidget, QMessageBox,
                           QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from ..config import APP_CONFIG, MANUFACTURERS, TAB_COLORS, UI_CONFIG, COLORS
from .dialogs import NewProjectDialog, StartupDialog
from .widgets import MaterialsTab, LaborWidget, SummaryWidget
from ..models import Project, TableauElectrique, Database
from ..utils.error_handler import ErrorHandler
from .dialogs.new_tableau import NewTableauDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.db = Database()
            self.project = None
            
            # Setup iniziale del progetto
            self.setup_project()
            
            if self.project:
                self.setWindowTitle(f"Preventivi Elettrici - Volta+ - {self.project.name}")
                self.setMinimumSize(UI_CONFIG['window_width'], UI_CONFIG['window_height'])
                
                self.setup_ui()
                
                # Timer per salvataggio automatico
                self.auto_save_timer = QTimer(self)
                self.auto_save_timer.timeout.connect(self.auto_save)
                self.auto_save_timer.start(APP_CONFIG['autosave_interval'])
            else:
                self.close()
        except Exception as e:
            logging.error(f"Errore nell'inizializzazione della MainWindow: {str(e)}")
            raise

    def setup_project(self):
        try:
            startup = StartupDialog()
            if startup.exec():
                if startup.action == "new":
                    self.project = Project(
                        name=startup.project_data['project_name'],
                        client_name=startup.project_data['client_name'],
                        volta_number=startup.project_data['volta_number']
                    )
                    # Crea quadri iniziali
                    for tableau_data in startup.project_data['tableaux']:
                        self.project.add_tableau(tableau_data['name'])
                else:
                    try:
                        self.project = Project.load_from_file(startup.project_data)
                    except Exception as e:
                        ErrorHandler.show_error(self, "Errore", 
                            "Errore durante il caricamento del progetto", e)
                        self.setup_project()  # Riprova
            else:
                sys.exit()
        except Exception as e:
            logging.error(f"Errore durante il setup del progetto: {str(e)}")
            raise

    def setup_ui(self):
        if not self.project:
            raise ValueError("Tentativo di setup UI senza un progetto valido")
            
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header con informazioni progetto
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(f"Progetto: {self.project.name}"))
        header_layout.addWidget(QLabel(f"Cliente: {self.project.client_name}"))
        header_layout.addWidget(QLabel(f"Volta: {self.project.volta_number}"))
        header_layout.addStretch()
        
        # Bottoni
        back_btn = QPushButton("Indietro")
        add_tableau_btn = QPushButton("Aggiungi Quadro")
        save_btn = QPushButton("Salva")
        export_btn = QPushButton("Esporta")
        
        back_btn.clicked.connect(self.go_back)
        add_tableau_btn.clicked.connect(self.add_new_tableau)
        save_btn.clicked.connect(lambda: self.save_project(True))
        export_btn.clicked.connect(self.export_project)
        
        header_layout.addWidget(back_btn)
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

    def add_tableau_tab(self, tableau: TableauElectrique):
        try:
            tab = QWidget()
            layout = QHBoxLayout(tab)
            
            # Tab per materiali
            materials_tabs = QTabWidget()
            materials_widgets = []
            
            # Crea un tab per ogni produttore
            for manufacturer in MANUFACTURERS:
                materials_tab = MaterialsTab(
                    parent=tab,
                    manufacturer=manufacturer,
                    database=self.db
                )
                materials_tab.dataChanged.connect(self.update_totals)
                materials_widgets.append(materials_tab)
                materials_tabs.addTab(materials_tab, manufacturer)
            
            layout.addWidget(materials_tabs, stretch=2)
            
            # Widget manodopera
            labor_widget = LaborWidget(parent=tab)
            labor_widget.dataChanged.connect(self.update_totals)
            layout.addWidget(labor_widget, stretch=1)
            
            # Widget riepilogo
            summary_widget = SummaryWidget(parent=tab)
            summary_widget.marginChanged.connect(self.update_totals)
            layout.addWidget(summary_widget, stretch=1)
            
            # Salva riferimenti ai widget nel tab
            tab.materials_tabs = materials_tabs
            tab.materials_widgets = materials_widgets
            tab.labor_widget = labor_widget
            tab.summary_widget = summary_widget
            
            # Aggiungi tab
            self.tableaux_tabs.addTab(tab, tableau.name)
        except Exception as e:
            logging.error(f"Errore nell'aggiunta del tab del quadro: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore nell'aggiunta del quadro: {str(e)}")

    def update_totals(self):
        try:
            current_tab = self.tableaux_tabs.currentWidget()
            if not current_tab:
                return

            # Calcola totali materiali
            material_total = 0
            time_total = 0
            modules_data = {
                'knx_modules': 0,
                'modules_05': 0,
                'modules_1p2p': 0,
                'modules_3p': 0,
                'modules_4p': 0,
                'total_modules': 0,
                'total_bornes': 0,
                'total_bornes_space': 0
            }

            # Raccolta dati da tutte le tabelle materiali
            for materials_tab in current_tab.materials_widgets:
                table = materials_tab.table
                manufacturer = materials_tab.manufacturer

                for row in range(table.rowCount()):
                    qty_item = table.item(row, 0)
                    price_total_item = table.item(row, 5)
                    time_total_item = table.item(row, 6)
                    modules_item = table.item(row, 7)
                    bornes_item = table.item(row, 8)
                    bornes_space_item = table.item(row, 10)

                    if all([qty_item, price_total_item]) and qty_item.text():
                        try:
                            qty = float(qty_item.text())
                            price_total = float(price_total_item.text().replace("'", ""))
                            material_total += price_total

                            if time_total_item and time_total_item.text():
                                time_total += float(time_total_item.text())

                            # Calcolo moduli
                            if modules_item and modules_item.text():
                                module_size = float(modules_item.text())
                                if manufacturer == 'KNX':
                                    modules_data['knx_modules'] += qty * module_size
                                if module_size == 0.5:
                                    modules_data['modules_05'] += qty
                                elif module_size in [1, 2]:
                                    modules_data['modules_1p2p'] += qty
                                elif module_size == 3:
                                    modules_data['modules_3p'] += qty
                                elif module_size >= 4:
                                    modules_data['modules_4p'] += qty
                                modules_data['total_modules'] += qty * module_size

                            # Calcolo bornes
                            if bornes_item and bornes_item.text():
                                modules_data['total_bornes'] += qty * float(bornes_item.text())
                            if bornes_space_item and bornes_space_item.text():
                                modules_data['total_bornes_space'] += qty * float(bornes_space_item.text())

                        except ValueError:
                            continue

            # Calcolo rangées
            if modules_data['total_modules'] > 0:
                modules_data['rangees'] = modules_data['total_modules'] * 1.3 / 80
                modules_data['rangees_24m'] = modules_data['total_modules'] * 1.3 / 24

            # Ottieni il costo della manodopera
            labor_total = current_tab.labor_widget.get_total_cost()

            # Aggiorna il riepilogo
            current_tab.summary_widget.update_costs(material_total, time_total, labor_total)
            current_tab.summary_widget.update_info(modules_data)
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento dei totali: {str(e)}")

    def save_project(self, show_message=True):
        try:
            filename = f"{self.project.name}.volta"
            self.project.save_to_file(filename)
            if show_message:
                QMessageBox.information(self, "Salvataggio",
                                    f"Progetto salvato in {filename}")
        except Exception as e:
            if show_message:
                QMessageBox.critical(self, "Errore",
                                f"Errore durante il salvataggio: {str(e)}")
            logging.error(f"Errore durante il salvataggio del progetto: {str(e)}")

    def auto_save(self):
        try:
            self.save_project(show_message=False)
        except Exception as e:
            logging.error(f"Errore nel salvataggio automatico: {str(e)}")

    def closeEvent(self, event):
        try:
            reply = QMessageBox.question(
                self,
                'Conferma chiusura',
                'Vuoi salvare il progetto prima di chiudere?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            logging.error(f"Errore durante la chiusura: {str(e)}")
            event.accept()

    def add_new_tableau(self):
        try:
            dialog = NewTableauDialog()
            if dialog.exec():
                data = dialog.get_data()
                if not data or 'name' not in data:
                    QMessageBox.warning(self, "Errore", "Dati del quadro non validi")
                    return

                tableau = self.project.add_tableau(data['name'])
                self.add_tableau_tab(tableau)
        except ValueError as e:
            QMessageBox.warning(self, "Errore", str(e))
        except Exception as e:
            logging.error(f"Errore durante l'aggiunta del nuovo quadro: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'aggiunta del quadro: {str(e)}")

    def close_tableau(self, index):
        try:
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
        except Exception as e:
            logging.error(f"Errore durante la chiusura del quadro: {str(e)}")

    def update_tab_color(self, manufacturer, has_content):
        try:
            current_tab = self.tableaux_tabs.currentWidget()
            if hasattr(current_tab, 'materials_tabs'):
                materials_tabs = current_tab.materials_tabs
                for i in range(materials_tabs.count()):
                    if materials_tabs.tabText(i) == manufacturer:
                        color = TAB_COLORS['with_content'] if has_content else TAB_COLORS['default']
                        materials_tabs.tabBar().setTabTextColor(i, QColor(color))
                        break
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento del colore del tab: {str(e)}")
                        
    def go_back(self):
        try:
            reply = QMessageBox.question(
                self,
                'Conferma',
                'Vuoi tornare alla schermata iniziale? Eventuali modifiche non salvate andranno perse.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.close()
                self.__init__()
        except Exception as e:
            logging.error(f"Errore durante il ritorno alla schermata iniziale: {str(e)}")

    def export_project(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Esporta Preventivo",
                f"Preventivo_{self.project.name}.xlsx",
                "Excel Files (*.xlsx)"
            )
            if filename:
                try:
                    # Implementa l'esportazione
                    QMessageBox.information(self, "Export",
                                        f"Preventivo esportato in {filename}")
                except Exception as e:
                    QMessageBox.critical(self, "Errore",
                                    f"Errore durante l'esportazione: {str(e)}")
        except Exception as e:
            logging.error(f"Errore durante l'esportazione: {str(e)}")