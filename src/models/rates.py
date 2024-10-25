from dataclasses import dataclass
from typing import Dict
from ..config import LABOR_BASE_RATES, LABOR_COEFFICIENTS, LaborType

@dataclass
class LaborRates:
    base_rates: Dict[str, float]
    current_type: LaborType
    
    def __init__(self, labor_type: LaborType = LaborType.INTERNAL):
        self.base_rates = LABOR_BASE_RATES.copy()
        self.current_type = labor_type
    
    def get_adjusted_rate(self, labor_name: str) -> float:
        base_rate = self.base_rates[labor_name]
        coefficient = LABOR_COEFFICIENTS[self.current_type][labor_name]
        return base_rate * coefficient
    
    def get_all_adjusted_rates(self) -> Dict[str, float]:
        return {name: self.get_adjusted_rate(name) for name in self.base_rates}
    
    def set_labor_type(self, labor_type: LaborType):
        self.current_type = labor_type
