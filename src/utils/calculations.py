
class MaterialCalculations:
    @staticmethod
    def calculate_material_totals(materials_data):
        """Calcola i totali per i materiali"""
        total_price = 0
        total_time = 0
        modules = {
            'knx': 0,
            '0.5m': 0,
            '1p2p': 0,
            '3p': 0,
            '4p': 0,
            'total': 0
        }
        bornes = {
            'count': 0,
            'space': 0
        }

        for row in materials_data:
            if not row['quantity']:
                continue

            quantity = float(row['quantity'])
            total_price += quantity * row['price']
            total_time += quantity * row['time']

            # Calcolo moduli
            if row['manufacturer'] == 'KNX':
                modules['knx'] += quantity * row['num_modules']
            
            module_size = row['num_modules']
            if module_size == 0.5:
                modules['0.5m'] += quantity
            elif module_size in [1, 2]:
                modules['1p2p'] += quantity
            elif module_size == 3:
                modules['3p'] += quantity
            elif module_size >= 4:
                modules['4p'] += quantity
            
            modules['total'] += quantity * module_size
            
            # Calcolo bornes
            if row['num_bornes']:
                bornes['count'] += quantity * row['num_bornes']
            if row['tot_bornes_mm']:
                bornes['space'] += quantity * row['tot_bornes_mm']

        # Calcolo rangées
        rangees = {
            'standard': modules['total'] * 1.3 / 80 if modules['total'] > 0 else 0,
            '24m': modules['total'] * 1.3 / 24 if modules['total'] > 0 else 0
        }

        return {
            'total_price': total_price,
            'total_time': total_time,
            'modules': modules,
            'bornes': bornes,
            'rangees': rangees
        }

class LaborCalculations:
    @staticmethod
    def calculate_labor_cost(labor_data, labor_type):
        """Calcola il costo totale della manodopera"""
        total_cost = 0
        for row in labor_data:
            if not row['hours']:
                continue
            
            hours = float(row['hours'])
            base_rate = row['rate']
            coefficient = labor_type.get_coefficient(row['type'])
            total_cost += hours * base_rate * coefficient
            
        return total_cost

class TotalCalculations:
    @staticmethod
    def calculate_final_totals(material_totals, labor_cost, material_margin):
        """Calcola i totali finali"""
        material_with_margin = material_totals['total_price'] * (1 + material_margin)
        total = material_with_margin + labor_cost
        
        return {
            'material_total': material_totals['total_price'],
            'material_with_margin': material_with_margin,
            'labor_total': labor_cost,
            'final_total': total
        }
