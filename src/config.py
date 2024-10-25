from enum import Enum

class LaborType(Enum):
    INTERNAL = "Interne"
    EXTERNAL = "Externe"
    BKW = "BKW"

TAB_COLORS = {
    'default': '#4CAF50',  # Verde
    'with_content': '#FF5722'  # Arancione
}
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

# Colori per i tab con contenuto
TAB_COLORS = {
    'default': '#4CAF50',
    'with_content': '#FF5722'
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

# Configurazioni database
DB_FILE = 'volta_plus.db'

# Manufacturers
MANUFACTURERS = ['Schneider', 'Hager', 'KNX', 'MCR', 'Swisspro']
