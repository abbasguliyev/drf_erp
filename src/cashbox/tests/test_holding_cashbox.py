from django.test import TestCase
from company.models import Holding
from cashbox.models import HoldingCashbox


class HoldingCashboxTest(TestCase):
    def setUp(self) -> None:
        #== Holding ==#
        self.holding = Holding.objects.create(name = 'Holding')
        self.holding.save()
        #== Holding Cashbox ==#
        self.holding_cashbox = HoldingCashbox.objects.create(
            title = 'Example',
            balance = 1000,
            note = 'Example note',
            holding = self.holding
        )
        self.holding_cashbox.save()

    def tearDown(self) -> None:
        self.holding.delete()

    def test_read_holding_cashbox(self):
        self.assertEqual(self.holding_cashbox.title, 'Example')
        self.assertEqual(self.holding_cashbox.balance, 1000)
        self.assertEqual(self.holding_cashbox.note, 'Example note')
        self.assertEqual(self.holding_cashbox.holding, self.holding)

    def test_update_holding_cashbox(self):
        self.holding_cashbox.title = 'New title'
        self.holding_cashbox.balance = 1500
        self.holding_cashbox.note = 'New note'
        self.holding_cashbox.save()

        self.assertEqual(self.holding_cashbox.title, 'New title')
        self.assertEqual(self.holding_cashbox.balance, 1500)
        self.assertEqual(self.holding_cashbox.note, 'New note')
    
    def test_update_related_datas(self):
        #== Holding ==#
        self.new_holding = Holding.objects.create(name = 'New holding')
        self.new_holding.save()
        #== Holding Cashbox ==#
        self.holding_cashbox.holding = self.new_holding
        self.holding_cashbox.save()
        #== Checking ==#
        self.assertEqual(self.holding_cashbox.holding, self.new_holding)
