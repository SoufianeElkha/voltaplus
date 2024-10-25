from typing import Dict, List, Tuple
import sqlite3
from src.config import APP_CONFIG, MANUFACTURERS

class Database:
    def __init__(self, db_file: str = None):
        self.db_file = db_file or APP_CONFIG['database_file']
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Prima elimina la tabella se esiste
            cursor.execute('DROP TABLE IF EXISTS products')
            
            # Crea tabella prodotti con colonne aggiuntive
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                reference TEXT PRIMARY KEY,
                designation TEXT,
                price REAL,
                time INTEGER,
                num_modules INTEGER,
                num_bornes INTEGER,
                bornes_mm REAL,
                tot_bornes_mm REAL,
                prix_2s REAL,
                prix_3s REAL,
                manufacturer TEXT
            )
            ''')
            
            # Dati di esempio per diversi produttori
            manufacturers_data = {
                'Schneider': [
                    ('A9F74206', 'iC60N 2P C 6A', 45.60, 15, 2, 4, 17.5, 70.0, 50.20, 55.80),
                    ('A9F74210', 'iC60N 2P C 10A', 48.90, 15, 2, 4, 17.5, 70.0, 53.80, 59.40),
                    ('A9F74216', 'iC60N 2P C 16A', 52.30, 15, 2, 4, 17.5, 70.0, 57.50, 63.30),
                    ('A9F74220', 'iC60N 2P C 20A', 55.70, 15, 2, 4, 17.5, 70.0, 61.30, 67.40),
                    ('A9F74225', 'iC60N 2P C 25A', 58.40, 15, 2, 4, 17.5, 70.0, 64.20, 70.60),
                ],
                'Hager': [
                    ('HTS263E', 'Interruttore 2P C 63A', 62.30, 20, 4, 6, 17.5, 105.0, 68.50, 75.40),
                    ('HTS240E', 'Interruttore 2P C 40A', 58.70, 20, 4, 6, 17.5, 105.0, 64.60, 71.20),
                    ('HTS232E', 'Interruttore 2P C 32A', 55.90, 20, 4, 6, 17.5, 105.0, 61.50, 67.70),
                    ('HTS225E', 'Interruttore 2P C 25A', 54.30, 20, 4, 6, 17.5, 105.0, 59.70, 65.70),
                ],
                'KNX': [
                    ('MTN6725-0001', 'KNX Power Supply 640mA', 385.0, 30, 4, 8, 17.5, 140.0, 423.50, 465.85),
                    ('MTN6003-0002', 'KNX IP Router', 420.0, 35, 2, 4, 17.5, 70.0, 462.00, 508.20),
                    ('MTN6164-0004', 'KNX Switch Actuator 4-fold', 275.0, 25, 4, 8, 17.5, 140.0, 302.50, 332.75),
                ],
                'MCR': [
                    ('MCR001', 'Relè di controllo', 145.30, 25, 2, 6, 17.5, 105.0, 159.83, 175.81),
                    ('MCR002', 'Timer digitale', 168.50, 28, 2, 4, 17.5, 70.0, 185.35, 203.89),
                    ('MCR003', 'Contatore energia', 195.70, 30, 4, 8, 17.5, 140.0, 215.27, 236.80),
                ],
                'Swisspro': [
                    ('SP001', 'Presa T13', 35.40, 10, 1, 3, 17.5, 52.5, 38.94, 42.83),
                    ('SP002', 'Interruttore', 42.60, 12, 1, 4, 17.5, 70.0, 46.86, 51.55),
                    ('SP003', 'Dimmer LED', 85.30, 15, 2, 6, 17.5, 105.0, 93.83, 103.21),
                ]
            }
            
            # Inserisci i dati per ogni produttore
            for manufacturer, products in manufacturers_data.items():
                for product in products:
                    cursor.execute('''
                    INSERT OR REPLACE INTO products 
                    (reference, designation, price, time, num_modules, num_bornes, 
                    bornes_mm, tot_bornes_mm, prix_2s, prix_3s, manufacturer)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (*product, manufacturer))
            
            conn.commit()
    
    def get_product(self, reference: str, manufacturer: str) -> Dict:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM products
            WHERE reference = ? AND manufacturer = ?
            ''', (reference, manufacturer))
            
            row = cursor.fetchone()
            if row:
                return {
                    'reference': row[0],
                    'designation': row[1],
                    'price': row[2],
                    'time': row[3],
                    'num_modules': row[4],
                    'num_bornes': row[5],
                    'bornes_mm': row[6],
                    'tot_bornes_mm': row[7],
                    'prix_2s': row[8],
                    'prix_3s': row[9],
                    'manufacturer': row[10]
                }
            return None

    def get_products_by_manufacturer(self, manufacturer: str) -> List[Dict]:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM products
            WHERE manufacturer = ?
            ORDER BY reference
            ''', (manufacturer,))
            
            products = []
            for row in cursor.fetchall():
                products.append({
                    'reference': row[0],
                    'designation': row[1],
                    'price': row[2],
                    'time': row[3],
                    'num_modules': row[4],
                    'num_bornes': row[5],
                    'bornes_mm': row[6],
                    'tot_bornes_mm': row[7],
                    'prix_2s': row[8],
                    'prix_3s': row[9],
                    'manufacturer': row[10]
                })
            return products

    def get_references_by_manufacturer(self, manufacturer: str) -> List[Tuple[str, str]]:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT reference, designation
            FROM products
            WHERE manufacturer = ?
            ORDER BY reference
            ''', (manufacturer,))
            return cursor.fetchall()