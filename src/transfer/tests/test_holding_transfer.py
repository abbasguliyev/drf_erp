from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from company.models import Company
from transfer.models import HoldingTransfer


User = get_user_model()

class HoldingTransferTest(TestCase):
    def setUp(self) -> None:
        #== Sending Company ==#
        self.sending_company = Company.objects.create(
            name = 'Company',
            address = 'Azərbaycan/Bakı',
            phone = '0503884575',
            email = 'example@example.com',
            web_site = 'https://www.example.com'
        )
        self.sending_company.save()
        #== Receiving Company ==#
        self.receiving_company = Company.objects.create(
            name = 'Receive',
            address = 'Azərbaycan/Sumqayıt',
            phone = '0706302454',
            email = 'receive@example.com',
            web_site = 'https://www.receive.com'
        )
        self.receiving_company.save()
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
        #== Holding Transfer ==#
        self.holding_transfer = HoldingTransfer.objects.create(
            transfer_amount = 1000,
            transfer_note = 'Example note',
            recipient_subsequent_balance = 2000,
            sender_subsequent_balance = 3000,
            executor = self.user,
            sending_company = self.sending_company,
            receiving_company = self.receiving_company
        )
        self.holding_transfer.save()

    def tearDown(self) -> None:
        self.sending_company.delete()
        self.receiving_company.delete()
        self.user.delete()
        self.holding_transfer.delete()

    def test_read_holding_transfer(self):
        self.assertEqual(self.holding_transfer.transfer_date, date.today())
        self.assertEqual(self.holding_transfer.transfer_amount, 1000)
        self.assertEqual(self.holding_transfer.transfer_note, 'Example note')
        self.assertEqual(self.holding_transfer.recipient_subsequent_balance, 2000)
        self.assertEqual(self.holding_transfer.sender_subsequent_balance, 3000)
        self.assertEqual(self.holding_transfer.executor, self.user)
        self.assertEqual(self.holding_transfer.sending_company, self.sending_company)
        self.assertEqual(self.holding_transfer.receiving_company, self.receiving_company)

    def test_update_holding_transfer(self):
        self.holding_transfer.transfer_amount = 1444
        self.holding_transfer.transfer_note = 'New example note'
        self.holding_transfer.recipient_subsequent_balance = 2888
        self.holding_transfer.sender_subsequent_balance = 7777

        self.assertNotEqual(self.holding_transfer.transfer_amount, 1000)
        self.assertEqual(self.holding_transfer.transfer_amount, 1444)
        self.assertNotEqual(self.holding_transfer.transfer_note, 'Example note')
        self.assertEqual(self.holding_transfer.transfer_note, 'New example note')
        self.assertNotEqual(self.holding_transfer.recipient_subsequent_balance, 2000)
        self.assertEqual(self.holding_transfer.recipient_subsequent_balance, 2888)
        self.assertNotEqual(self.holding_transfer.sender_subsequent_balance, 3000)
        self.assertEqual(self.holding_transfer.sender_subsequent_balance, 7777)

    def test_update_related_datas(self):
        #== Sending Company ==#
        self.new_sending_company = Company.objects.create(
            name = 'New company',
            address = 'Azərbaycan/Gəncə',
            phone = '0776985642',
            email = 'new@example.com',
            web_site = 'https://www.new.com'
        )
        self.new_sending_company.save()
        #== Receiving Company ==#
        self.new_receiving_company = Company.objects.create(
            name = 'New receive company',
            address = 'Azərbaycan/İmişli',
            phone = '0557100606',
            email = 'newreceive@example.com',
            web_site = 'https://www.newreceive.com'
        )
        self.new_receiving_company.save()
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
        #== Holding Transfer ==#
        self.holding_transfer.executor = self.new_user
        self.holding_transfer.sending_company = self.new_sending_company
        self.holding_transfer.receiving_company = self.new_receiving_company
        self.holding_transfer.save()
        #== Checking ==#
        self.assertNotEqual(self.holding_transfer.executor, self.user)
        self.assertEqual(self.holding_transfer.executor, self.new_user)
        self.assertNotEqual(self.holding_transfer.sending_company, self.sending_company)
        self.assertEqual(self.holding_transfer.sending_company, self.new_sending_company)
        self.assertNotEqual(self.holding_transfer.receiving_company, self.receiving_company)
        self.assertEqual(self.holding_transfer.receiving_company, self.new_receiving_company)
