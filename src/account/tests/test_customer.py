from django.test import TestCase
from account.models import (
    Customer,
    Region
)


class CustomerTest(TestCase):
    def setUp(self) -> None:
        #== Region ==#
        self.region = Region.objects.create(region_name = 'Bakı')
        self.region.save()
        #== Customer ==#
        self.customer = Customer.objects.create(
            fullname = 'Customer',
            email = 'customer@example.com',
            profile_image = None,
            photo_ID = None,
            back_photo_of_ID = None,
            phone_number_1 = '0996357421',
            phone_number_2 = '0709195363',
            phone_number_3 = '0554457585',
            phone_number_4 = '0518804433',
            address = 'Azərbaycan/Sumqayıt',
            note = "Customer's note.",
            is_active = True,
            region = self.region
        )
        self.customer.save()

    def tearDown(self) -> None:
        self.customer.delete()
    
    def test_read_customer(self):
        self.assertEqual(self.customer.fullname, 'Customer')
        self.assertEqual(self.customer.email, 'customer@example.com')
        self.assertEqual(self.customer.phone_number_1, '0996357421')
        self.assertEqual(self.customer.phone_number_2, '0709195363')
        self.assertEqual(self.customer.phone_number_3, '0554457585')
        self.assertEqual(self.customer.phone_number_4, '0518804433')
        self.assertEqual(self.customer.address, 'Azərbaycan/Sumqayıt')
        self.assertEqual(self.customer.note, "Customer's note.")
        self.assertTrue(self.customer.is_active)
        self.assertEqual(self.customer.region, self.region)

    def test_update_customer(self):
        #== Customer ==#
        self.customer.fullname = 'New_Customer'
        self.customer.phone_number_1 = '+905046357'
        self.customer.phone_number_2 = '+902132965'
        self.customer.phone_number_3 = '+905079686'
        self.customer.phone_number_4 = '+908034545'
        self.customer.address = 'Türkiyə/Ankara'
        self.customer.email = 'new_customer@example.com'
        self.customer.note = "(NEW)Customer's note."
        self.customer.save()
        #== Checking ==#
        self.assertEqual(self.customer.fullname, 'New_Customer')
        self.assertEqual(self.customer.phone_number_1, '+905046357')
        self.assertEqual(self.customer.phone_number_2, '+902132965')
        self.assertEqual(self.customer.phone_number_3, '+905079686')
        self.assertEqual(self.customer.phone_number_4, '+908034545')
        self.assertEqual(self.customer.address, 'Türkiyə/Ankara')
        self.assertEqual(self.customer.email, 'new_customer@example.com')
        self.assertEqual(self.customer.note, "(NEW)Customer's note.")

    def test_update_related_datas(self):
        #== Region ==#
        self.region_new = Region.objects.create(region_name = 'Sumqayıt')
        self.region_new.save()
        #== Customer ==#
        self.customer.region = self.region_new
        self.customer.save()
        #== Checking ==#
        self.assertEqual(self.customer.region, self.region_new)

    def test_update_customer_is_active(self):
        self.customer.is_active = False
        self.customer.save()
        self.assertFalse(self.customer.is_active)
