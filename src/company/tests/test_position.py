from django.test import TestCase
from company.models import Position


class PositionTest(TestCase):
    def setUp(self) -> None:
        self.position = Position(name="POSITION")
        self.position.save()
    
    def tearDown(self) -> None:
        self.position.delete()
    
    def test_read_position(self):
        self.assertEqual(self.position.name, "POSITION")
        self.assertTrue(self.position.is_active)
    
    def test_update_position_name(self):
        self.position.name = "POSITION2"
        self.position.save()
        self.assertEqual(self.position.name, "POSITION2")
    
    def test_update_position_is_active(self):
        self.position.is_active =False
        self.position.save()
        self.assertFalse(self.position.is_active)
