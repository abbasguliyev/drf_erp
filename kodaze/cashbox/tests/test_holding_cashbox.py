from django.test import TestCase
from company.models import Holding
from cashbox.models import (
    HoldingCashbox,
)


class HoldingCashboxTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding.objects.create(name="Holding")
        self.holding.save()
        self.holding_cashbox = HoldingCashbox(
            holding=self.holding,
            balance=1000
        )
        self.holding_cashbox.save()

    def tearDown(self) -> None:
        self.holding.delete()

    def test_read_holding_cashbox(self):
        self.assertEqual(self.holding_cashbox.balance, 1000)
        self.assertEqual(self.holding_cashbox.holding.name, "Holding")

    def test_update_holding_cashbox(self):
        self.holding_cashbox.balance = 1500
        self.holding_cashbox.save()
        
        self.assertEqual(self.holding_cashbox.balance, 1500)
