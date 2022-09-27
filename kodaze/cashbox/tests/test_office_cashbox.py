from django.test import TestCase
from company.models import Company, Holding, Office
from cashbox.models import (
    OfficeCashbox,
)


class OfficeCashboxTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding.objects.create(name="Holding")
        self.holding.save()
        self.company = Company.objects.create(
            name="Company", holding=self.holding)
        self.company.save()
        self.office = Office.objects.create(name="Baku", company=self.company)
        self.office.save()
        self.office_cashbox = OfficeCashbox(
            office=self.office,
            balance=1000
        )
        self.office_cashbox.save()

    def tearDown(self) -> None:
        self.holding.delete()

    def test_read_office_cashbox(self):
        self.assertEqual(self.office_cashbox.balance, 1000)
        self.office_cashbox.save()
        self.assertEqual(self.office_cashbox.office.name, "Baku")

    def test_update_office_cashbox(self):
        self.office_cashbox.balance = 1500
        self.office_cashbox.save()
        self.assertEqual(self.office_cashbox.balance, 1500)
