from django.test import TestCase
from company.models import Company


class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.company = Company(
            name = 'Company',
            address = 'address',
            phone = '0553137963',
            email = 'email@gmail.com',
            web_site = 'https://www.google.com'
        )
        self.company.save()
    
    def tearDown(self) -> None:
        self.company.delete()
    
    def test_read_company(self):
        self.assertEqual(self.company.name, 'Company')
        self.assertEqual(self.company.address, 'address')
        self.assertEqual(self.company.phone, '0553137963')
        self.assertEqual(self.company.email, 'email@gmail.com')
        self.assertEqual(self.company.web_site, 'https://www.google.com')
        self.assertTrue(self.company.is_active)
    
    def test_update_company(self):
        self.company.name = 'Company2'
        self.company.address = 'address2'
        self.company.phone = '0709192969'
        self.company.email = 'admin@gmail.com'
        self.company.web_site = 'https://www.facebook.com'
        self.company.save()
    
        self.assertEqual(self.company.name, 'Company2')
        self.assertEqual(self.company.address, 'address2')
        self.assertEqual(self.company.phone, '0709192969')
        self.assertEqual(self.company.email, 'admin@gmail.com')
        self.assertEqual(self.company.web_site, 'https://www.facebook.com')
    
    def test_update_company_is_active(self):
        self.company.is_active = False
        self.company.save()
        self.assertFalse(self.company.is_active)
