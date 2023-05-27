from django.test import TestCase
from product.models import Category


class CategoryTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(
            category_name = 'Maye'
        )
        self.category.save()
    
    def tearDown(self) -> None:
        self.category.delete()
    
    def test_read_category(self):
        self.assertEqual(self.category.category_name, 'Maye')
    
    def test_update_category(self):
        self.category.category_name = 'Bərk'
        self.assertEqual(self.category.category_name, 'Bərk')
