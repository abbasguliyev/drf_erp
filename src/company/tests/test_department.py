from django.test import TestCase
from company.models import Department


class DepartmentTest(TestCase):
    def setUp(self) -> None:
        self.department = Department(name="Department")
        self.department.save()
    
    def tearDown(self) -> None:
        self.department.delete()
    
    def test_read_department(self):
        self.assertEqual(self.department.name, "Department")
        self.assertTrue(self.department.is_active)
    
    def test_update_department_name(self):
        self.department.name = "Department2"
        self.department.save()
        self.assertEqual(self.department.name, "Department2")
    
    def test_update_department_is_active(self):
        self.department.is_active =False
        self.department.save()
        self.assertFalse(self.department.is_active)
