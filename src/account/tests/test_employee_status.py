from django.test import TestCase
from account.models import (
    EmployeeStatus
)


class EmployeeStatusTest(TestCase):
    def setUp(self) -> None:
        self.employee_status = EmployeeStatus.objects.create(status_name='Standart')
        self.employee_status.save()

    def tearDown(self) -> None:
        self.employee_status.delete()

    def test_read_employee_status(self):
        self.assertEqual(self.employee_status.status_name, 'Standart')

    def test_update_employee_status(self):
        self.employee_status.status_name = "Bronze"
        self.employee_status.save()
        self.assertEqual(self.employee_status.status_name, 'Bronze')
