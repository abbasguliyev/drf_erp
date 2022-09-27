from django.test import TestCase
from company.models import Holding, Company, Office, Section

class DepartmentTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding(name="Holding")
        self.holding.save()
        self.company = Company(name="Company", holding=self.holding)
        self.company.save()
        self.office = Office(name="Office", company=self.company)
        self.office.save()
        self.section = Section(name="Section", office=self.office)
        self.section.save()
        
    def tearDown(self) -> None:
        self.holding.delete()
        
    def test_read_section(self):
        self.assertEqual(self.section.name, "Section")
        self.assertEqual(self.section.office, self.office)
        self.assertEqual(self.section.is_active, True)
    
    def test_update_section_name(self):
        self.section.name = "Section2"
        self.section.save()
        self.assertEqual(self.section.name, "Section2")
        
    def test_update_section_is_active(self):
        self.section.is_active =False
        self.section.save()
        self.assertEqual(self.section.is_active, False)
        
    