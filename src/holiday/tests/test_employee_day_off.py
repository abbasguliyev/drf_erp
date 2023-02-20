from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from holiday.models import (
    EmployeeDayOff,
    EmployeeDayOffHistory
)


User = get_user_model()

class EmployeeDayOffTest(TestCase):
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
        #== Employee Day Off ==#
        self.employee_day_off = EmployeeDayOff.objects.create(
            employee = self.user,
            history = self.employee_day_off_history,
            day_off_date = date(2023, 1, 20),
            is_paid = True,
            paid_amount = 150
        )
        self.employee_day_off.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.employee_day_off_history.delete()
        self.employee_day_off.delete()

    def test_read_employee_day_off(self):
        self.assertEqual(self.employee_day_off.employee, self.user)
        self.assertEqual(self.employee_day_off.history, self.employee_day_off_history)
        self.assertEqual(self.employee_day_off.day_off_date, date(2023, 1, 20))
        self.assertTrue(self.employee_day_off.is_paid)
        self.assertEqual(self.employee_day_off.paid_amount, 150)

    def test_update_employee_day_off(self):
        today = date.today()
        self.employee_day_off.day_off_date = today
        self.employee_day_off.is_paid = False
        self.employee_day_off.paid_amount = 300

        self.assertNotEqual(self.employee_day_off.day_off_date, date(2023, 1, 20))
        self.assertEqual(self.employee_day_off.day_off_date, today)
        self.assertFalse(self.employee_day_off.is_paid)
        self.assertNotEqual(self.employee_day_off.paid_amount, 150)
        self.assertEqual(self.employee_day_off.paid_amount, 300)

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
        self.new_employee_day_off_history = EmployeeDayOffHistory.objects.create(
            employee = self.new_user,
            note = 'New example note',
            is_paid = False
        )
        self.new_employee_day_off_history.save()
        #== Employee Day Off ==#
        self.employee_day_off.employee = self.new_user
        self.employee_day_off.history = self.new_employee_day_off_history
        #== Checking ==#
        self.assertNotEqual(self.employee_day_off.employee, self.user)
        self.assertEqual(self.employee_day_off.employee, self.new_user)
        self.assertNotEqual(self.employee_day_off.history, self.employee_day_off_history)
        self.assertEqual(self.employee_day_off.history, self.new_employee_day_off_history)
