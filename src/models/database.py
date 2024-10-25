import sqlite3
from typing import Dict, List, Tuple
from src.config import DB_FILE, MANUFACTURERS
class Database:
    def __init__(self, db_file: str = 'volta_plus.db'):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Crea tabella prodotti se non esiste
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
            
            # Inserisci dati di esempio se la tabella è vuota
            cursor.execute('SELECT COUNT(*) FROM products')
            if cursor.fetchone()[0] == 0:
                self._insert_sample_data(cursor)
            
            conn.commit()
    
    def _insert_sample_data(self, cursor):
        manufacturers_data = {
            'Schneider': [
                ('A9F74206', 'iC60N 2P C 6A', 45.60, 15, 2, 4, 17.5, 70.0, 50.20, 55.80),
                ('A9F74210', 'iC60N 2P C 10A', 48.90, 15, 2, 4, 17.5, 70.0, 53.80, 59.40),
                # Aggiungi altri prodotti qui
            ],
            'Hager': [
                ('HTS263E', 'Interruttore 2P C 63A', 62.30, 20, 4, 6, 17.5, 105.0, 68.50, 75.40),
                # Aggiungi altri prodotti qui
            ],
            # Aggiungi altri produttori qui
        }
        
        for manufacturer, products in manufacturers_data.items():
            for product in products:
                cursor.execute('''
                INSERT OR REPLACE INTO products 
                (reference, designation, price, time, num_modules, num_bornes, 
                bornes_mm, tot_bornes_mm, prix_2s, prix_3s, manufacturer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (*product, manufacturer))
    
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