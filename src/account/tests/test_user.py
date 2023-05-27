from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from datetime import datetime
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from account.models import (
    Region,
    EmployeeStatus
)
from company.models import (
    Company,
    Office,
    Department,
    Position
)
from salary.models import Commission


User = get_user_model()

class UserTest(TestCase):
    def setUp(self) -> None:
        #== Region ==#
        self.region = Region.objects.create(region_name = 'Bakı')
        self.region.save()
        #== Company ==#
        self.company = Company.objects.create(
            name = 'Example',
            address = 'Azərbaycan/Bakı/Xocasən',
            phone = '0773285697',
            email = 'example@gmail.com',
            web_site = 'https://www.example.com',
            is_active = True
        )
        self.company.save()
        #== Office ==#
        self.office = Office.objects.create(
            name = 'Abşeron',
            company = self.company,
            is_active = True
        )
        self.office.save()
        #== Department ==#
        self.department = Department.objects.create(
            name = 'XY',
            is_active = True
        )
        self.department.save()
        #== Position ==#
        self.position = Position.objects.create(
            name = 'Backend',
            is_active = True
        )
        self.position.save()
        #== EmployeeStatus ==#
        self.employee_status = EmployeeStatus.objects.create(
            status_name = 'Example'
        )
        self.employee_status.save()
        #== Commission ==#
        self.commission = Commission.objects.create(
            commission_name = 'Example',
            for_office = 1.2,
            cash = 1.2,
            for_team = 1.2,
            creditor_per_cent = 10
        )
        self.commission.save()

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
            employee_status = self.employee_status,
            commission = self.commission,
            region = self.region,
            company = self.company,
            office = self.office,
            department = self.department,
            position = self.position
        )
        self.user.save()
    
    def tearDown(self) -> None:
        self.user.delete()

    def test_login(self):
        user = authenticate(username = 'admin', password = 'Admin123!')
        self.assertTrue((user is not None) and user.is_authenticated)
    
    def test_read_user(self):
        self.assertEqual(self.user.username, 'admin')
        self.assertEqual(self.user.fullname, 'X Y Z')
        self.assertEqual(self.user.phone_number_1, '0557894561')
        self.assertEqual(self.user.phone_number_2, '0517894561')
        self.assertEqual(self.user.address, 'Azərbaycan/Bakı/28May')
        self.assertEqual(self.user.email, 'example@example.com')
        self.assertEqual(self.user.note, 'Example note.')
        self.assertEqual(self.user.salary, 500.36)
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.salary_style, 'Kommissiya')
        self.assertEqual(self.user.register_type, 'Holding')
        self.assertEqual(self.user.employee_status, self.employee_status)
        self.assertEqual(self.user.commission, self.commission)
        self.assertEqual(self.user.region, self.region)
        self.assertEqual(self.user.company, self.company)
        self.assertEqual(self.user.office, self.office)
        self.assertEqual(self.user.department, self.department)
        self.assertEqual(self.user.position, self.position)

    def test_update_user(self):
        #== User ==#
        self.user.username = 'new_admin'
        self.user.fullname = 'N E W'
        self.user.phone_number_1 = '+905046357'
        self.user.phone_number_2 = '+902132965'
        self.user.address = 'Türkiyə/Iğdır'
        self.user.email = 'new_example@example.com'
        self.user.note = '(NEW)Example note.'
        self.user.salary = 1320.44
        self.user.save()
        #== Checking ==#
        self.assertEqual(self.user.username, 'new_admin')
        self.assertEqual(self.user.fullname, 'N E W')
        self.assertEqual(self.user.phone_number_1, '+905046357')
        self.assertEqual(self.user.phone_number_2, '+902132965')
        self.assertEqual(self.user.address, 'Türkiyə/Iğdır')
        self.assertEqual(self.user.email, 'new_example@example.com')
        self.assertEqual(self.user.note, '(NEW)Example note.')
        self.assertEqual(self.user.salary, 1320.44)

    def test_update_related_datas(self):
        #== Region ==#
        self.region_new = Region.objects.create(region_name = 'Sumqayıt')
        self.region_new.save()
        #== Company ==#
        self.company_new = Company.objects.create(
            name = 'Example(NEW)',
            address = 'Azərbaycan/Gəncə',
            phone = '0504658965',
            email = 'new_user@gmail.com',
            web_site = 'https://www.example_new.com',
            is_active = True
        )
        self.company_new.save()
        #== Office ==#
        self.office_new = Office.objects.create(
            name = 'Sumqayıt',
            company = self.company,
            is_active = True
        )
        self.office_new.save()
        #== Department ==#
        self.department_new = Department.objects.create(
            name = 'NEW',
            is_active = True
        )
        self.department_new.save()
        #== Position ==#
        self.position_new = Position.objects.create(
            name = 'FRONTEND',
            is_active = True
        )
        self.position_new.save()
        #== EmployeeStatus ==#
        self.employee_status_new = EmployeeStatus.objects.create(
            status_name = 'Example(NEW)'
        )
        self.employee_status_new.save()
        #== Commission ==#
        self.commission_new = Commission.objects.create(
            commission_name = 'Example(NEW)',
            for_office = 3.4,
            cash = 3.4,
            for_team = 3.4,
            creditor_per_cent = 25
        )
        self.commission_new.save()
        #== User ==#
        self.user.salary_style = SALARY_STYLE_CHOICES[0][0]
        self.user.register_type = REGISTER_TYPE_CHOICES[1][0]
        self.user.employee_status = self.employee_status_new
        self.user.commission = self.commission_new
        self.user.region = self.region_new
        self.user.company = self.company_new
        self.user.office = self.office_new
        self.user.department = self.department_new
        self.user.position = self.position_new
        self.user.save()
        #== Checking ==#
        self.assertEqual(self.user.salary_style, 'Fix+Kommissiya')
        self.assertEqual(self.user.register_type, 'Şirkət')
        self.assertEqual(self.user.employee_status, self.employee_status_new)
        self.assertEqual(self.user.commission, self.commission_new)
        self.assertEqual(self.user.region, self.region_new)
        self.assertEqual(self.user.company, self.company_new)
        self.assertEqual(self.user.office, self.office_new)
        self.assertEqual(self.user.department, self.department_new)
        self.assertEqual(self.user.position, self.position_new)

    def test_update_user_is_active(self):
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.user.is_active)

    def test_date_fields(self):
        #== Today ==#
        today = datetime.now().strftime('%d-%m-%Y')
        self.assertEqual(self.user.contract_date.strftime('%d-%m-%Y'), today)
        self.assertEqual(self.user.date_joined.strftime('%d-%m-%Y'), today)
