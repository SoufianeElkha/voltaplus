
from enum import Enum

class LaborType(Enum):
    INTERNAL = "Interne"
    EXTERNAL = "Externe"
    BKW = "BKW"

# Tariffe base
LABOR_BASE_RATES = {
    "Chef Projet": 64.00,
    "Chef Atelier": 64.00,
    "Montage Câblage": 57.00,
    "Schéma": 64.00,
    "Relevé": 57.00,
    "Transport": 57.00,
    "Pose": 57.00
}

# Coefficienti per tipo di manodopera
LABOR_COEFFICIENTS = {
    LaborType.INTERNAL: {
        "Chef Projet": 1.3,
        "Chef Atelier": 1.3,
        "Montage Câblage": 1.25,
        "Schéma": 1.5,
        "Relevé": 1.43,
        "Transport": 1.25,
        "Pose": 1.25
    },
    LaborType.EXTERNAL: {
        "Chef Projet": 1.46,
        "Chef Atelier": 1.46,
        "Montage Câblage": 1.43,
        "Schéma": 1.61,
        "Relevé": 1.43,
        "Transport": 1.43,
        "Pose": 1.43
    },
    LaborType.BKW: {
        "Chef Projet": 1.38,
        "Chef Atelier": 1.38,
        "Montage Câblage": 1.34,
        "Schéma": 1.61,
        "Relevé": 1.34,
        "Transport": 1.34,
        "Pose": 1.34
    }
}

# Struttura del sommario
SUMMARY_SECTIONS = {
    'costs': [
        "Total Matériel",
        "Total Temps",
        "Total Main d'Œuvre",
        "Total Final"
    ],
    'info_tableau': [
        "Tot Modules KNX",
        "Qté 0,5M",
        "Qté 1P/1P+N/2P",
        "Qté 3P/3P+N",
        "Qté 4P/+4P",
        "Rangées + 30%",
        "Rangées 24M +30%",
        "Tot Modules",
        "Tot Bornes",
        "Tot Espace Bornes"
    ]
}

# Configurazioni dell'applicazione
APP_CONFIG = {
    'database_file': 'volta_plus.db',
    'log_file': 'volta_plus.log',
    'autosave_interval': 300000,  # 5 minuti in millisecondi
    'default_margin': 25.0,
    'project_file_extension': '.volta'
}

# Lista dei produttori
MANUFACTURERS = ['Schneider', 'Hager', 'KNX', 'MCR', 'Swisspro']

# Configurazioni UI
UI_CONFIG = {
    'window_width': 1600,
    'window_height': 900,
    'table_row_height': 25,
    'min_button_width': 80,
    'margin_decimals': 2
}

# Colori
COLORS = {
    'primary': '#4CAF50',
    'primary_dark': '#388E3C',
    'primary_light': '#C8E6C9',
    'secondary': '#2196F3',
    'secondary_dark': '#1976D2',
    'warning': '#FF5722',
    'background': '#f5f5f5',
    'surface': '#FFFFFF',
    'border': '#ddd',
    'text': '#333333',
    'text_light': '#FFFFFF'
}

# Colori dei tab
TAB_COLORS = {
    'default': '#4CAF50',  # Verde
    'with_content': '#FF5722'  # Arancione
}
