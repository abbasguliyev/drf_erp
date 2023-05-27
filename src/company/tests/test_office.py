from django.test import TestCase
from company.models import Company, Office


class OfficeTest(TestCase):
    def setUp(self) -> None:
        self.company = Company(name="Company")
        self.company.save()
        self.office = Office(name="Office", company=self.company)
        self.office.save()
    
    def tearDown(self) -> None:
        self.company.delete()
        self.office.delete()
    
    def test_read_office(self):
        self.assertEqual(self.office.name, "Office")
        self.assertEqual(self.office.company, self.company)
        self.assertTrue(self.office.is_active)
    
    def test_update_office_name(self):
        self.office.name = "Office2"
        self.office.save()
        self.assertEqual(self.office.name, "Office2")
    
    def test_update_office_is_active(self):
        self.office.is_active =False
        self.office.save()
        self.assertFalse(self.office.is_active)
