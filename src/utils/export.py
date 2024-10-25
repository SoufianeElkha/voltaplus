
import pandas as pd
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

class ExcelExporter:
    def __init__(self, project):
        self.project = project
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        self.header_fill = PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")
        self.header_font = Font(color="FFFFFF", bold=True)

    def export(self, filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            self._write_info_sheet(writer)
            
            for tableau_name, tableau in self.project.tableaux.items():
                self._write_materials_sheet(writer, tableau_name, tableau)
                self._write_labor_sheet(writer, tableau_name, tableau)
                self._write_summary_sheet(writer, tableau_name, tableau)
            
            self._apply_styles(writer)

    def _write_info_sheet(self, writer):
        info_data = {
            'Progetto': [self.project.name],
            'Cliente': [self.project.client_name],
            'Numero Volta': [self.project.volta_number],
            'Data Creazione': [self.project.creation_date]
        }
        df = pd.DataFrame(info_data)
        df.to_excel(writer, sheet_name='Info Progetto', index=False)

    def _write_materials_sheet(self, writer, tableau_name, tableau):
        if not tableau.materials_data:
            return
        
        df = pd.DataFrame(tableau.materials_data)
        sheet_name = f'{tableau_name} - Materiali'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Formattazione condizionale
        sheet = writer.sheets[sheet_name]
        for column in df.columns:
            col_idx = df.columns.get_loc(column) + 1
            col_letter = get_column_letter(col_idx)
            max_length = max(df[column].astype(str).apply(len).max(),
                           len(column))
            sheet.column_dimensions[col_letter].width = max_length + 2

    def _write_labor_sheet(self, writer, tableau_name, tableau):
        if not tableau.labor_data:
            return
        
        df = pd.DataFrame(tableau.labor_data)
        sheet_name = f'{tableau_name} - Manodopera'
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    def _write_summary_sheet(self, writer, tableau_name, tableau):
        if not tableau.summary_data:
            return
        
        df = pd.DataFrame(tableau.summary_data)
        sheet_name = f'{tableau_name} - Riepilogo'
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    def _apply_styles(self, writer):
        for sheet in writer.sheets.values():
            for cell in sheet[1]:  # Header row
                cell.fill = self.header_fill
                cell.font = self.header_font
                cell.alignment = Alignment(horizontal='center')
                cell.border = self.border

            for row in sheet.iter_rows(min_row=2):
                for cell in row:
                    cell.border = self.border
                    cell.alignment = Alignment(horizontal='left')
