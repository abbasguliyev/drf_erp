from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from holiday.models import EmployeeWorkingDay


User = get_user_model()

class EmployeeWorkingDayTest(TestCase):
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
        #== Employee Working Day ==#
        self.employee_working_day = EmployeeWorkingDay.objects.create(
            employee = self.user,
            working_days_count = 20,
            date = date.today()
        )
        self.employee_working_day.save()

    def tearDown(self) -> None:
        self.user.delete()
        self.employee_working_day.delete()
    
    def test_read_employee_working_day(self):
        self.assertEqual(self.employee_working_day.employee, self.user)
        self.assertEqual(self.employee_working_day.working_days_count, 20)
        self.assertEqual(self.employee_working_day.date, date.today())

    def test_update_employee_working_day(self):
        specific_date = date(2023, 1, 25)
        self.employee_working_day.working_days_count = 30
        self.employee_working_day.date = specific_date

        self.assertNotEqual(self.employee_working_day.working_days_count, 20)
        self.assertEqual(self.employee_working_day.working_days_count, 30)
        self.assertNotEqual(self.employee_working_day.date, date.today())
        self.assertEqual(self.employee_working_day.date, specific_date)
    
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
        #== Employee Working Day ==#
        self.employee_working_day.employee = self.new_user
        #== Checking ==#
        self.assertNotEqual(self.employee_working_day.employee, self.user)
        self.assertEqual(self.employee_working_day.employee, self.new_user)
