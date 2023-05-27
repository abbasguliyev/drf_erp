from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from holiday.models import EmployeeDayOffHistory


User = get_user_model()

class EmployeeDayOffHistoryTest(TestCase):
    def setUp(self) -> None:
        #== User ==#
        self.user = User.objects.create_user(
            username = 'admin',
            password = 'Admin123!',
            fullname = 'X Y Z',
            phone_number_1 = '0557894561',
            phone_number_2 = '0517894561',
            address = 'Azərbaycan/Bakı/28May',
            email = 'example@example.com',
            note = 'Example note.',
            salary = 500.36,
            photo_ID = None,
            back_photo_of_ID = None,
            driving_license_photo = None,
            electronic_signature = None,
            profile_image = None,
            is_active = True,
            salary_style = SALARY_STYLE_CHOICES[1][0],
            register_type = REGISTER_TYPE_CHOICES[0][0],
        )
        self.user.save()
        #== Employee Day Off History ==#
        self.employee_day_off_history = EmployeeDayOffHistory.objects.create(
            employee = self.user,
            note = 'Example note',
            is_paid = True
        )
        self.employee_day_off_history.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.employee_day_off_history.delete()

    def test_read_employee_day_off_history(self):
        self.assertEqual(self.employee_day_off_history.employee, self.user)
        self.assertEqual(self.employee_day_off_history.created_date, date.today())
        self.assertEqual(self.employee_day_off_history.note, 'Example note')
        self.assertTrue(self.employee_day_off_history.is_paid)

    def test_update_employee_day_off_history(self):
        self.employee_day_off_history.note = 'New example note'
        self.employee_day_off_history.is_paid = False

        self.assertNotEqual(self.employee_day_off_history.note, 'Example note')
        self.assertEqual(self.employee_day_off_history.note, 'New example note')
        self.assertFalse(self.employee_day_off_history.is_paid)

    def test_update_related_datas(self):
        #== User ==#
        self.new_user = User.objects.create_user(
            username = 'new_admin',
            password = 'New_Admin123!',
            fullname = 'N E W',
            phone_number_1 = '+905046357',
            phone_number_2 = '+902132965',
            address = 'Türkiyə/Iğdır',
            email = 'new_example@example.com',
            note = 'NEW)Example note.',
            salary = 700,
            photo_ID = None,
            back_photo_of_ID = None,
            driving_license_photo = None,
            electronic_signature = None,
            profile_image = None,
            is_active = True,
            salary_style = SALARY_STYLE_CHOICES[0][0],
            register_type = REGISTER_TYPE_CHOICES[1][0]
        )
        self.new_user.save()
        #== Employee Day Off History ==#
        self.employee_day_off_history.employee = self.new_user
        #== Checking ==#
        self.assertNotEqual(self.employee_day_off_history.employee, self.user)
        self.assertEqual(self.employee_day_off_history.employee, self.new_user)
