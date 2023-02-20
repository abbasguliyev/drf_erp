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
from transfer.models import CompanyTransfer


User = get_user_model()

class CompanyTransferTest(TestCase):
    def setUp(self) -> None:
        #== Company ==#
        self.company = Company.objects.create(
            name = 'Company',
            address = 'Azərbaycan/Bakı',
            phone = '0503884575',
            email = 'example@example.com',
            web_site = 'https://www.example.com'
        )
        self.company.save()
        #== Sending Office ==#
        self.sending_office = Office.objects.create(
            name = "X1",
            company = self.company
        )
        self.sending_office.save()
        #== Receiving Office ==#
        self.receiving_office = Office.objects.create(
            name = "X2",
            company = self.company
        )
        self.receiving_office.save()
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
            register_type = REGISTER_TYPE_CHOICES[0][0]
        )
        self.user.save()
        #== Company Transfer ==#
        self.company_transfer = CompanyTransfer.objects.create(
            transfer_amount = 1000,
            transfer_note = 'Example note',
            recipient_subsequent_balance = 2000,
            sender_subsequent_balance = 3000,
            executor = self.user,
            company = self.company,
            sending_office = self.sending_office,
            receiving_office = self.receiving_office
        )
        self.company_transfer.save()

    def tearDown(self) -> None:
        self.company.delete()
        self.sending_office.delete()
        self.receiving_office.delete()
        self.user.delete()
        self.company_transfer.delete()

    def test_read_company_transfer(self):
        self.assertEqual(self.company_transfer.transfer_date, date.today())
        self.assertEqual(self.company_transfer.transfer_amount, 1000)
        self.assertEqual(self.company_transfer.transfer_note, 'Example note')
        self.assertEqual(self.company_transfer.recipient_subsequent_balance, 2000)
        self.assertEqual(self.company_transfer.sender_subsequent_balance, 3000)
        self.assertEqual(self.company_transfer.executor, self.user)
        self.assertEqual(self.company_transfer.company, self.company)
        self.assertEqual(self.company_transfer.sending_office, self.sending_office)
        self.assertEqual(self.company_transfer.receiving_office, self.receiving_office)

    def test_update_company_transfer(self):
        self.company_transfer.transfer_amount = 1444
        self.company_transfer.transfer_note = 'New example note'
        self.company_transfer.recipient_subsequent_balance = 2888
        self.company_transfer.sender_subsequent_balance = 7777

        self.assertNotEqual(self.company_transfer.transfer_amount, 1000)
        self.assertEqual(self.company_transfer.transfer_amount, 1444)
        self.assertNotEqual(self.company_transfer.transfer_note, 'Example note')
        self.assertEqual(self.company_transfer.transfer_note, 'New example note')
        self.assertNotEqual(self.company_transfer.recipient_subsequent_balance, 2000)
        self.assertEqual(self.company_transfer.recipient_subsequent_balance, 2888)
        self.assertNotEqual(self.company_transfer.sender_subsequent_balance, 3000)
        self.assertEqual(self.company_transfer.sender_subsequent_balance, 7777)

    def test_update_related_datas(self):
        #== Company ==#
        self.new_company = Company.objects.create(
            name = 'New_company',
            address = 'Azərbaycan/Sumqayıt',
            phone = '0776985642',
            email = 'new@example.com',
            web_site = 'https://www.new.com'
        )
        self.new_company.save()
        #== Sending Office ==#
        self.new_sending_office = Office.objects.create(
            name = "New X1",
            company = self.new_company
        )
        self.new_sending_office.save()
        #== Receiving Office ==#
        self.new_receiving_office = Office.objects.create(
            name = "New X2",
            company = self.new_company
        )
        self.new_receiving_office.save()
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
        #== Company Transfer ==#
        self.company_transfer.executor = self.new_user
        self.company_transfer.company = self.new_company
        self.company_transfer.sending_office = self.new_sending_office
        self.company_transfer.receiving_office = self.new_receiving_office
        self.company_transfer.save()
        #== Checking ==#
        self.assertNotEqual(self.company_transfer.executor, self.user)
        self.assertEqual(self.company_transfer.executor, self.new_user)
        self.assertNotEqual(self.company_transfer.company, self.company)
        self.assertEqual(self.company_transfer.company, self.new_company)
        self.assertNotEqual(self.company_transfer.sending_office, self.sending_office)
        self.assertEqual(self.company_transfer.sending_office, self.new_sending_office)
        self.assertNotEqual(self.company_transfer.receiving_office, self.receiving_office)
        self.assertEqual(self.company_transfer.receiving_office, self.new_receiving_office)
