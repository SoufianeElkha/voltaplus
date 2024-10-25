import unittest
from src.models import Project, TableauElectrique, Database
from src.config import MANUFACTURERS

class TestVoltaPlus(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')  # Database in memoria per i test
        self.project = Project(
            name="Test Project",
            client_name="Test Client",
            volta_number="TEST001"
        )

    def test_database_initialization(self):
        """Verifica che il database sia inizializzato correttamente"""
        # Verifica che ci siano prodotti per ogni produttore
        for manufacturer in MANUFACTURERS:
            products = self.db.get_products_by_manufacturer(manufacturer)
            self.assertTrue(len(products) > 0)

    def test_project_creation(self):
        """Verifica la creazione di un progetto"""
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.client_name, "Test Client")

    def test_tableau_creation(self):
        """Verifica l'aggiunta di un quadro"""
        tableau = self.project.add_tableau("Test Tableau")
        self.assertIn("Test Tableau", self.project.tableaux)
        self.assertEqual(len(self.project.tableaux), 1)

if __name__ == '__main__':
    unittest.main()