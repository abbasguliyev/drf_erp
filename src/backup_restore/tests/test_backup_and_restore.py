from django.test import TestCase
from datetime import date
from backup_restore.models import BackupAndRestore


class BackupAndRestoreTest(TestCase):
    def setUp(self) -> None:
        self.backup_and_restore = BackupAndRestore.objects.create(
            backup_date = date(2023, 1, 3),
            restore_date = date(2023, 1, 4),
            media_backup_date = date(2023, 1, 5)
        )

    def tearDown(self) -> None:
        self.backup_and_restore.delete()
    
    def test_read_backup_and_restore(self):
        self.assertEqual(self.backup_and_restore.backup_date, date(2023, 1, 3))
        self.assertEqual(self.backup_and_restore.restore_date, date(2023, 1, 4))
        self.assertEqual(self.backup_and_restore.media_backup_date, date(2023, 1, 5))

    def test_update_backup_and_restore(self):
        self.backup_and_restore.backup_date = date(2022, 12, 17)
        self.backup_and_restore.restore_date = date(2022, 12, 20)
        self.backup_and_restore.media_backup_date = date(2022, 12, 30)
        self.backup_and_restore.save()

        self.assertEqual(self.backup_and_restore.backup_date, date(2022, 12, 17))
        self.assertEqual(self.backup_and_restore.restore_date, date(2022, 12, 20))
        self.assertEqual(self.backup_and_restore.media_backup_date, date(2022, 12, 30))
