from django.test import TestCase
from company.models import Company, Holding
from cashbox.models import (
    CompanyCashbox,
)


class CompanyCashboxTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding.objects.create(name="Holding")
        self.holding.save()
        self.company = Company.objects.create(
            name="Company", holding=self.holding)
        self.company.save()
        self.company_cashbox = CompanyCashbox(
            company=self.company,
            balance=1000
        )
        self.company_cashbox.save()

    def tearDown(self) -> None:
        self.holding.delete()

    def test_read_company_cashbox(self):
        self.assertEqual(self.company_cashbox.balance, 1000)
        self.assertEqual(self.company_cashbox.company.name, "Company")

    def test_update_company_cashbox(self):
        self.company_cashbox.balance = 1500
        self.company_cashbox.save()
        self.assertEqual(self.company_cashbox.balance, 1500)
