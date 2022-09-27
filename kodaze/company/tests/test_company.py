from django.test import TestCase
from company.models import Holding, Company

class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding(name="Holding")
        self.holding.save()
        self.company = Company(name="Company", holding=self.holding)
        self.company.save()
        
    def tearDown(self) -> None:
        self.holding.delete()
        
    def test_read_company(self):
        self.assertEqual(self.company.name, "Company")
        self.assertEqual(self.company.holding, self.holding)
        self.assertEqual(self.company.is_active, True)
    
    def test_update_company_name(self):
        self.company.name = "Company2"
        self.company.save()
        self.assertEqual(self.company.name, "Company2")
        
    def test_update_company_is_active(self):
        self.company.is_active =False
        self.company.save()
        self.assertEqual(self.company.is_active, False)
        
    