from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from holiday.models import (
    EmployeeHoliday,
    EmployeeHolidayHistory
)


User = get_user_model()

class EmployeeHolidayTest(TestCase):
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
        #== Employee Holiday History ==#
        self.employee_holiday_history = EmployeeHolidayHistory.objects.create(
            employee = self.user,
            note = 'Example note'
        )
        self.employee_holiday_history.save()
        #== Employee Holiday ==#
        self.employee_holiday = EmployeeHoliday.objects.create(
            employee = self.user,
            history = self.employee_holiday_history,
            holiday_date = date(2023, 12, 31)
        )
        self.employee_holiday.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.employee_holiday_history.delete()
        self.employee_holiday.delete()

    def test_read_employee_holiday(self):
        self.assertEqual(self.employee_holiday.employee, self.user)
        self.assertEqual(self.employee_holiday.history, self.employee_holiday_history)
        self.assertEqual(self.employee_holiday.holiday_date, date(2023, 12, 31))

    def test_update_employee_holiday(self):
        self.employee_holiday.holiday_date = date(2024, 1, 1)
        
        self.assertNotEqual(self.employee_holiday.holiday_date, date(2023, 12, 31))
        self.assertEqual(self.employee_holiday.holiday_date, date(2024, 1, 1))

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
            register_type = REGISTER_TYPE_CHOICES[1][0],
        )
        self.new_user.save()
        #== Employee Holiday History ==#
        self.new_employee_holiday_history = EmployeeHolidayHistory.objects.create(
            employee = self.new_user,
            note = 'New example note'
        )
        self.new_employee_holiday_history.save()
        #== Employee Holiday ==#
        self.employee_holiday.employee = self.new_user
        self.employee_holiday.history = self.new_employee_holiday_history
        #== Checking ==#
        self.assertNotEqual(self.employee_holiday.employee, self.user)
        self.assertEqual(self.employee_holiday.employee, self.new_user)
        self.assertNotEqual(self.employee_holiday.history, self.employee_holiday_history)
        self.assertEqual(self.employee_holiday.history, self.new_employee_holiday_history)
