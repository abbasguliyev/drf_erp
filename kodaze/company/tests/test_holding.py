from django.test import TestCase
from company.models import Holding

class HoldingTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding(name="Holding")
        self.holding.save()
        
    def tearDown(self) -> None:
        self.holding.delete()
        
    def test_read_holding(self):
        self.assertEqual(self.holding.name, "Holding")
        self.assertEqual(self.holding.is_active, True)
    
    def test_update_holding_name(self):
        self.holding.name = "Holding2"
        self.holding.save()
        self.assertEqual(self.holding.name, "Holding2")
        
    def test_update_holding_is_active(self):
        self.holding.is_active =False
        self.holding.save()
        self.assertEqual(self.holding.is_active, False)
        
    