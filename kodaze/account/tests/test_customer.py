from django.test import TestCase
from account.models import (
    Customer,
    Region
)
from django.contrib.auth import get_user_model

class CustomerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="admin", password="Admin123!")
        self.user.save()
        self.region = Region(region_name="Baku")
        self.region.save()
        self.customer = Customer(
            fullname="Name Surname Fathername",
            phone_number_1="123456",
            email="test@gmail.com",
            address="Test",
            region=self.region,
            note="Test Note",
            order_count=0
        )
        self.customer.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.customer.delete()
        self.region.delete()

    def test_read_customer(self):
        self.assertEqual(self.customer.fullname, "Name Surname Fathername")
        self.assertEqual(self.customer.phone_number_1, "123456")
        self.assertEqual(self.customer.email, "test@gmail.com")
        self.assertEqual(self.customer.address, "Test")
        self.assertEqual(self.customer.region, self.region)
        self.assertEqual(self.customer.note, "Test Note")
        self.assertEqual(self.customer.is_active, True)

    def test_customer_is_active(self):
        self.assertEqual(self.customer.is_active, True)

    def test_update_customer_is_active(self):
        self.customer.is_active = False
        self.assertEqual(self.customer.is_active, False)
