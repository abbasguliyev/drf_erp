from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from holiday.models import EmployeeHolidayHistory


User = get_user_model()

class EmployeeHolidayHistoryTest(TestCase):
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

    def tearDown(self) -> None:
        self.user.delete()
        self.employee_holiday_history.delete()

    def test_read_employee_holiday_history(self):
        self.assertEqual(self.employee_holiday_history.employee, self.user)
        self.assertEqual(self.employee_holiday_history.note, 'Example note')

    def test_update_employee_holiday_history(self):
        self.employee_holiday_history.note = 'New example note'
        
        self.assertNotEqual(self.employee_holiday_history.note, 'Example note')
        self.assertEqual(self.employee_holiday_history.note, 'New example note')

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
        self.employee_holiday_history.employee = self.new_user
        #== Checking ==#
        self.assertNotEqual(self.employee_holiday_history.employee, self.user)
        self.assertEqual(self.employee_holiday_history.employee, self.new_user)

    def test_date_fields(self):
        #== Today ==#
        today = datetime.now().strftime('%d-%m-%Y')
        self.assertEqual(self.employee_holiday_history.created_date.strftime('%d-%m-%Y'), today)
