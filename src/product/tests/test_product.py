from django.test import TestCase
from product.models import (
    UnitOfMeasure,
    Category,
    Product
)


class ProductTest(TestCase):
    def setUp(self) -> None:
        #== Unit Of Measure ==#
        self.unit_of_measure = UnitOfMeasure.objects.create(
            name = 'Litr'
        )
        self.unit_of_measure.save()
        #== Category ==#
        self.category = Category.objects.create(
            category_name = 'Maye'
        )
        self.category.save()
        #== Product ==#
        self.product = Product.objects.create(
            product_name = 'Coca-Cola',
            barcode = 123456789,
            purchase_price = 1,
            price = 1.50,
            guarantee = 1,
            is_gift = False,
            weight = 0.1,
            width = 10,
            length = 25,
            height = 25,
            volume = 5,
            note = 'Example note',
            category = self.category,
            unit_of_measure = self.unit_of_measure
        )
        self.product.save()
    
    def tearDown(self) -> None:
        self.unit_of_measure.delete()
        self.category.delete()
        self.product.delete()
    
    def test_read_product(self):
        self.assertEqual(self.product.product_name, 'Coca-Cola')
        self.assertEqual(self.product.barcode, 123456789)
        self.assertEqual(self.product.purchase_price, 1)
        self.assertEqual(self.product.price, 1.50)
        self.assertEqual(self.product.guarantee, 1)
        self.assertFalse(self.product.is_gift)
        self.assertEqual(self.product.weight, 0.1)
        self.assertEqual(self.product.width, 10)
        self.assertEqual(self.product.length, 25)
        self.assertEqual(self.product.height, 25)
        self.assertEqual(self.product.volume, 5)
        self.assertEqual(self.product.note, 'Example note')
        self.assertEqual(self.product.unit_of_measure, self.unit_of_measure)
        self.assertEqual(self.product.category, self.category)
    
    def test_update_product(self):
        self.product.product_name = 'Pepsi'
        self.product.barcode = 987654321
        self.product.purchase_price = 0.7
        self.product.price = 1.25
        self.product.guarantee = 2
        self.product.is_gift = True
        self.product.weight = 0.2
        self.product.width = 12
        self.product.length = 22
        self.product.height = 22
        self.product.volume = 10
        self.product.note = 'New example note'

        self.assertEqual(self.product.product_name, 'Pepsi')
        self.assertEqual(self.product.barcode, 987654321)
        self.assertEqual(self.product.purchase_price, 0.7)
        self.assertEqual(self.product.price, 1.25)
        self.assertEqual(self.product.guarantee, 2)
        self.assertTrue(self.product.is_gift)
        self.assertEqual(self.product.weight, 0.2)
        self.assertEqual(self.product.width, 12)
        self.assertEqual(self.product.length, 22)
        self.assertEqual(self.product.height, 22)
        self.assertEqual(self.product.volume, 10)
        self.assertEqual(self.product.note, 'New example note')
    
    def test_update_related_datas(self):
        #== Unit Of Measure ==#
        self.new_unit_of_measure = UnitOfMeasure.objects.create(
            name = 'Kiloqram'
        )
        self.new_unit_of_measure.save()
        #== Category ==#
        self.new_category = Category.objects.create(
            category_name = 'Bərk'
        )
        self.new_category.save()
        #== Product ==#
        self.product.unit_of_measure = self.new_unit_of_measure
        self.product.category = self.new_category
        #== Checking ==#
        self.assertEqual(self.product.unit_of_measure, self.new_unit_of_measure)
        self.assertEqual(self.product.category, self.new_category)
