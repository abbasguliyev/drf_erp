from django.test import TestCase
from update.models import Update


class UpdateTest(TestCase):
    def setUp(self) -> None:
        self.update = Update.objects.create(
            update_name = 'Example name',
            update_description = 'Example description',
            update_version = 'Example version'
        )
        self.update.save()
    
    def tearDown(self) -> None:
        self.update.delete()
    
    def test_read_update(self):
        self.assertEqual(self.update.update_name, 'Example name')
        self.assertEqual(self.update.update_description, 'Example description')
        self.assertEqual(self.update.update_version, 'Example version')
    
    def test_update_update(self):
        self.update.update_name = 'New name'
        self.update.update_description = 'New description'
        self.update.update_version = 'New version'
        self.update.save()

        self.assertEqual(self.update.update_name, 'New name')
        self.assertEqual(self.update.update_description, 'New description')
        self.assertEqual(self.update.update_version, 'New version')
