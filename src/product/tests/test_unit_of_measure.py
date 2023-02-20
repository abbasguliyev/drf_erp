from django.test import TestCase
from product.models import UnitOfMeasure


class UnitOfMeasureTest(TestCase):
    def setUp(self) -> None:
        self.unit_of_measure = UnitOfMeasure.objects.create(
            name = 'Litr'
        )
        self.unit_of_measure.save()
    
    def tearDown(self) -> None:
        self.unit_of_measure.delete()
    
    def test_read_unit_of_measure(self):
        self.assertEqual(self.unit_of_measure.name, 'Litr')
    
    def test_update_unit_of_measure(self):
        self.unit_of_measure.name = 'Kiloqram'
        self.assertEqual(self.unit_of_measure.name, 'Kiloqram')
