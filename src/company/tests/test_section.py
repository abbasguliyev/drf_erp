from django.test import TestCase
from company.models import Section


class SectionTest(TestCase):
    def setUp(self) -> None:
        self.section = Section(name="Section")
        self.section.save()
    
    def tearDown(self) -> None:
        self.section.delete()
    
    def test_read_section(self):
        self.assertEqual(self.section.name, "Section")
        self.assertTrue(self.section.is_active)
    
    def test_update_section_name(self):
        self.section.name = "Section2"
        self.section.save()
        self.assertEqual(self.section.name, "Section2")
        
    def test_update_section_is_active(self):
        self.section.is_active =False
        self.section.save()
        self.assertFalse(self.section.is_active)
