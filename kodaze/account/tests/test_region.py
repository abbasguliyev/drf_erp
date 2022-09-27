from django.test import TestCase
from account.models import (
    Region
)


class RegionTest(TestCase):
    def setUp(self) -> None:
        self.region = Region(region_name="Baku")
        self.region.save()

    def tearDown(self) -> None:
        self.region.delete()

    def test_read_region(self):
        self.assertEqual(self.region.region_name, "Baku")

    def test_update_region_region_name(self):
        self.region.region_name = "Sumgait"
        self.region.save()
        self.assertEqual(self.region.region_name, "Sumgait")
