from dataclasses import dataclass, field
from typing import List, Dict
import json
from datetime import datetime

@dataclass
class TableauElectrique:
    name: str
    materials_data: Dict = field(default_factory=dict)
    labor_data: List = field(default_factory=list)
    summary_data: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'name': self.name,
            'materials_data': self.materials_data,
            'labor_data': self.labor_data,
            'summary_data': self.summary_data
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            materials_data=data.get('materials_data', {}),
            labor_data=data.get('labor_data', []),
            summary_data=data.get('summary_data', {})
        )

@dataclass
class Project:
    name: str
    client_name: str
    volta_number: str
    creation_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    tableaux: Dict[str, TableauElectrique] = field(default_factory=dict)
    
    def add_tableau(self, name: str) -> TableauElectrique:
        """Aggiunge un nuovo quadro al progetto"""
        if name in self.tableaux:
            raise ValueError(f"Quadro '{name}' già esistente in questo progetto")
        tableau = TableauElectrique(name=name)
        self.tableaux[name] = tableau
        return tableau
    
    def remove_tableau(self, name: str):
        """Rimuove un quadro dal progetto"""
        if name in self.tableaux:
            del self.tableaux[name]
    
    def save_to_file(self, filename: str):
        """Salva il progetto su file"""
        data = {
            'name': self.name,
            'client_name': self.client_name,
            'volta_number': self.volta_number,
            'creation_date': self.creation_date,
            'tableaux': {name: tableau.to_dict() for name, tableau in self.tableaux.items()}
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filename: str):
        """Carica il progetto da file"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        project = cls(
            name=data['name'],
            client_name=data['client_name'],
            volta_number=data['volta_number'],
            creation_date=data.get('creation_date', datetime.now().strftime("%Y-%m-%d"))
        )
        for name, tableau_data in data['tableaux'].items():
            project.tableaux[name] = TableauElectrique.from_dict(tableau_data)
        return project
