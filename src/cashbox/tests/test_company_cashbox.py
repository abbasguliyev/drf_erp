from django.test import TestCase
from company.models import Company
from cashbox.models import CompanyCashbox


class CompanyCashboxTest(TestCase):
    def setUp(self) -> None:
        #== Company ==#
        self.company = Company.objects.create(
            name='Company',
            address = 'Azərbaycan/Bakı',
            phone = '0503884575',
            email = 'example@example.com',
            web_site = 'https://www.example.com',
        )
        self.company.save()
        #== Company Cashbox ==#
        self.company_cashbox = CompanyCashbox.objects.create(
            title = 'Example',
            balance = 1000,
            note = 'Example note',
            company = self.company
        )
        self.company_cashbox.save()

    def tearDown(self) -> None:
        self.company.delete()

    def test_read_company_cashbox(self):
        self.assertEqual(self.company_cashbox.title, 'Example')
        self.assertEqual(self.company_cashbox.balance, 1000)
        self.assertEqual(self.company_cashbox.note, 'Example note')
        self.assertEqual(self.company_cashbox.company, self.company)

    def test_update_company_cashbox(self):
        self.company_cashbox.title = 'New title'
        self.company_cashbox.balance = 1500
        self.company_cashbox.note = 'New note'
        self.company_cashbox.save()

        self.assertEqual(self.company_cashbox.title, 'New title')
        self.assertEqual(self.company_cashbox.balance, 1500)
        self.assertEqual(self.company_cashbox.note, 'New note')

    def test_update_related_datas(self):
        #== Company ==#
        self.new_company = Company.objects.create(
            name = 'New_company',
            address = 'Azərbaycan/Sumqayıt',
            phone = '0776985642',
            email = 'new@example.com',
            web_site = 'https://www.new.com',
        )
        self.new_company.save()
        #== Office Cashbox ==#
        self.company_cashbox.company = self.new_company
        self.company_cashbox.save()
        #== Checking ==#
        self.assertEqual(self.company_cashbox.company, self.new_company)
