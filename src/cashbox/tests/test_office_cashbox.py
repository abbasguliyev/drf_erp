from django.test import TestCase
from company.models import (
    Company,
    Office
)
from cashbox.models import OfficeCashbox


class OfficeCashboxTest(TestCase):
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
        #== Office ==#
        self.office = Office.objects.create(name="Baku", company = self.company)
        self.office.save()
        #== Office Cashbox ==#
        self.office_cashbox = OfficeCashbox.objects.create(
            title = 'Example',
            balance = 1000,
            note = 'Example note',
            office = self.office
        )
        self.office_cashbox.save()

    def tearDown(self) -> None:
        self.company.delete()

    def test_read_office_cashbox(self):
        self.assertEqual(self.office_cashbox.title, 'Example')
        self.assertEqual(self.office_cashbox.balance, 1000)
        self.assertEqual(self.office_cashbox.note, 'Example note')
        self.assertEqual(self.office_cashbox.office, self.office)

    def test_update_office_cashbox(self):
        self.office_cashbox.title = 'New title'
        self.office_cashbox.balance = 1500
        self.office_cashbox.note = 'New note'
        self.office_cashbox.save()

        self.assertEqual(self.office_cashbox.title, 'New title')
        self.assertEqual(self.office_cashbox.balance, 1500)
        self.assertEqual(self.office_cashbox.note, 'New note')

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
        #== Office ==#
        self.new_office = Office.objects.create(name="Sumqayıt", company=self.company)
        self.new_office.save()
        #== Office Cashbox ==#
        self.office_cashbox.office = self.new_office
        self.office_cashbox.save()
        #== Checking ==#
        self.assertEqual(self.office_cashbox.office, self.new_office)
