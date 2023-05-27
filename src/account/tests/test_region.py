from django.test import TestCase
from account.models import (
    Region
)


class RegionTest(TestCase):
    def setUp(self) -> None:
        self.region = Region.objects.create(region_name="Bakı")
        self.region.save()

    def tearDown(self) -> None:
        self.region.delete()

    def test_read_region(self):
        self.assertEqual(self.region.region_name, "Bakı")

    def test_update_region(self):
        self.region.region_name = "Sumqayıt"
        self.region.save()
        self.assertEqual(self.region.region_name, "Sumqayıt")
