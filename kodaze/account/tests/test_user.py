from django.test import TestCase
from account.models import (
    Customer,
    Region
)
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="admin", password="Admin123!")
        self.user.save()

    def test_read_user(self):
        self.assertEqual(self.user.username, "admin")