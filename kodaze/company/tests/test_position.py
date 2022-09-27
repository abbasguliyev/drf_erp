from django.test import TestCase
from company.models import Position

class PositionTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding(name="Holding")
        self.holding.save()
        self.company = Company(name="Company", holding=self.holding)
        self.company.save()
        self.position = Position(company=company, name="Position")
        self.position.save()
        
    def tearDown(self) -> None:
        self.position.delete()
        
    def test_read_position(self):
        self.assertEqual(self.position.name, "POSITION")
        self.assertEqual(self.position.is_active, True)
    
    def test_update_position_name(self):
        self.position.name = "position2"
        self.position.save()
        self.assertEqual(self.position.name, "POSITION2")
        
    def test_update_position_is_active(self):
        self.position.is_active =False
        self.position.save()
        self.assertEqual(self.position.is_active, False)
        
    def test_save_method_position(self):
        self.position.name = "position3"
        self.position.save()
        self.assertEqual(self.position.name, "POSITION3")