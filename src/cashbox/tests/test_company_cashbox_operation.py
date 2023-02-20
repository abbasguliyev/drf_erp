from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from company.models import (
    Company,
    Office
)
from cashbox import OPERATION_STYLE_CHOICE
from cashbox.models import CompanyCashboxOperation


User = get_user_model()

class CompanyCashboxOperationTest(TestCase):
    def setUp(self) -> None:
        #== Company ==#
        self.company = Company.objects.create(
            name='Company',
            address = 'Azərbaycan/Bakı',
            phone = '0503884575',
            email = 'example@example.com',
            web_site = 'https://www.example.com',
        )
        self.company.save()
        #== Office ==#
        self.office = Office.objects.create(
            name = "Gəncə",
            company = self.company
        )
        self.office.save()
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
            salary = 500,
            photo_ID = None,
            back_photo_of_ID = None,
            driving_license_photo = None,
            electronic_signature = None,
            profile_image = None,
            is_active = True,
            salary_style = SALARY_STYLE_CHOICES[1][0],
            register_type = REGISTER_TYPE_CHOICES[0][0]
        )
        self.user.save()
        #== Company Cashbox Operation ==#
        self.company_cashbox_operation = CompanyCashboxOperation.objects.create(
            amount = 1000,
            note = 'Example note',
            operation = OPERATION_STYLE_CHOICE[0][0],
            executor = self.user,
            personal = self.user,
            company = self.company,
            office = self.office
        )
        self.company_cashbox_operation.save()

    def tearDown(self) -> None:
        self.company.delete()
        self.office.delete()
        self.user.delete()
        self.company_cashbox_operation.delete()
    
    def test_read_company_cashbox_operation(self):
        self.assertEqual(self.company_cashbox_operation.date, date.today())
        self.assertEqual(self.company_cashbox_operation.amount, 1000)
        self.assertEqual(self.company_cashbox_operation.note, 'Example note')
        self.assertEqual(self.company_cashbox_operation.operation, 'MƏDAXİL')
        self.assertEqual(self.company_cashbox_operation.executor, self.user)
        self.assertEqual(self.company_cashbox_operation.personal, self.user)
        self.assertEqual(self.company_cashbox_operation.company, self.company)
        self.assertEqual(self.company_cashbox_operation.office, self.office)

    def test_update_company_cashbox_operation(self):
        self.company_cashbox_operation.amount = 3400
        self.company_cashbox_operation.note = 'New example note'
        self.company_cashbox_operation.save()
    
    def test_update_related_datas(self):
        #== Company ==#
        self.new_company = Company.objects.create(
            name = 'New_company',
            address = 'Azərbaycan/Sumqayıt',
            phone = '0776985642',
            email = 'new@example.com',
            web_site = 'https://www.new.com',
        )
        self.new_company.save()
        #== Office ==#
        self.new_office = Office.objects.create(
            name = 'Sumqayıt',
            company = self.new_company
        )
        self.new_office.save()
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
        #== Holding Cashbox Operation ==#
        self.company_cashbox_operation.operation = OPERATION_STYLE_CHOICE[1][0]
        self.company_cashbox_operation.company = self.new_company
        self.company_cashbox_operation.office = self.new_office
        self.company_cashbox_operation.executor = self.new_user
        self.company_cashbox_operation.personal = self.new_user
        self.company_cashbox_operation.save()
        #== Checking ==#
        self.assertEqual(self.company_cashbox_operation.operation, 'MƏXARİC')
        self.assertEqual(self.company_cashbox_operation.company, self.new_company)
        self.assertEqual(self.company_cashbox_operation.office, self.new_office)
        self.assertEqual(self.company_cashbox_operation.executor, self.new_user)
        self.assertEqual(self.company_cashbox_operation.personal, self.new_user)