from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from cashbox.models import CashFlow
from cashbox import OPERATION_STYLE_CHOICE
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from account.models import (
    Customer,
    Region
)
from company.models import (
    Company,
    Holding,
    Office
)


User = get_user_model()

class CashFlowTest(TestCase):
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
        #== Holding ==#
        self.holding = Holding.objects.create(
            name = 'Holding'
        )
        self.holding.save()
        #== Office ==#
        self.office = Office.objects.create(
            name = "Gəncə",
            company = self.company
        )
        self.office.save()
        #== Region ==#
        self.region = Region.objects.create(
            region_name = 'Bakı'
        )
        self.region.save()
        #== Customer ==#
        self.customer = Customer.objects.create(
            fullname = 'Customer',
            email = 'customer@example.com',
            profile_image = None,
            photo_ID = None,
            back_photo_of_ID = None,
            phone_number_1 = '0996357421',
            phone_number_2 = '0709195363',
            phone_number_3 = '0554457585',
            phone_number_4 = '0518804433',
            address = 'Azərbaycan/Sumqayıt',
            note = "Customer's note.",
            region = self.region
        )
        self.customer.save()
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
            region = self.region,
            company = self.company,
            office = self.office
        )
        self.user.save()
        #== Cash Flow ==#
        self.cash_flow = CashFlow.objects.create(
            date = date.today(),
            description = 'Example description',
            balance = 1000,
            quantity = 3,
            operation_style = OPERATION_STYLE_CHOICE[0][0],
            holding = self.holding,
            company = self.company,
            office = self.office,
            customer = self.customer,
            personal = self.user,
            executor = self.user
        )
        self.cash_flow.save()

    def tearDown(self) -> None:
        self.company.delete()
        self.holding.delete()
        self.office.delete()
        self.region.delete()
        self.customer.delete()
        self.user.delete()
        self.cash_flow.delete()
    
    def test_read_cash_flow(self):
        self.assertEqual(self.cash_flow.date, date.today())
        self.assertEqual(self.cash_flow.description, 'Example description')
        self.assertEqual(self.cash_flow.balance, 1000)
        self.assertEqual(self.cash_flow.quantity, 3)
        self.assertEqual(self.cash_flow.operation_style, 'MƏDAXİL')
        self.assertEqual(self.cash_flow.holding, self.holding)
        self.assertEqual(self.cash_flow.company, self.company)
        self.assertEqual(self.cash_flow.office, self.office)
        self.assertEqual(self.cash_flow.customer, self.customer)
        self.assertEqual(self.cash_flow.personal, self.user)
        self.assertEqual(self.cash_flow.executor, self.user)

    def test_update_cash_flow(self):
        specific_date = date(2023, 12, 25)
        self.cash_flow.date = specific_date
        self.cash_flow.description = 'New description'
        self.cash_flow.balance = 1500
        self.cash_flow.quantity = 1
        self.cash_flow.save()

        self.assertEqual(self.cash_flow.date, specific_date)
        self.assertEqual(self.cash_flow.description, 'New description')
        self.assertEqual(self.cash_flow.balance, 1500)
        self.assertEqual(self.cash_flow.quantity, 1)
    
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
        #== Holding ==#
        self.new_holding = Holding.objects.create(
            name = 'New holding'
        )
        self.new_holding.save()
        #== Office ==#
        self.new_office = Office.objects.create(
            name = 'Sumqayıt',
            company = self.new_company
        )
        self.new_office.save()
        #== Region ==#
        self.new_region = Region.objects.create(
            region_name = 'İmişli'
        )
        self.new_region.save()
        #== Customer ==#
        self.new_customer = Customer.objects.create(
            fullname = 'New_Customer',
            email = 'new_customer@example.com',
            profile_image = None,
            photo_ID = None,
            back_photo_of_ID = None,
            phone_number_1 = '+905046357',
            phone_number_2 = '+902132965',
            phone_number_3 = '+905079686',
            phone_number_4 = '+908034545',
            address = 'Türkiyə/Ankara',
            note = "(NEW)Customer's note.",
            region = self.new_region
        )
        self.new_customer.save()
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
            region = self.new_region,
            company = self.new_company,
            office = self.new_office
        )
        self.new_user.save()
        #== Cash Flow ==#
        self.cash_flow.operation_style = OPERATION_STYLE_CHOICE[1][0]
        self.cash_flow.holding = self.new_holding
        self.cash_flow.company = self.new_company
        self.cash_flow.office = self.new_office
        self.cash_flow.customer = self.new_customer
        self.cash_flow.personal = self.new_user
        self.cash_flow.executor = self.new_user
        self.cash_flow.save()
        #== Checking ==#
        self.assertEqual(self.cash_flow.operation_style, 'MƏXARİC')
        self.assertEqual(self.cash_flow.holding, self.new_holding)
        self.assertEqual(self.cash_flow.company, self.new_company)
        self.assertEqual(self.cash_flow.office, self.new_office)
        self.assertEqual(self.cash_flow.customer, self.new_customer)
        self.assertEqual(self.cash_flow.personal, self.new_user)
        self.assertEqual(self.cash_flow.executor, self.new_user)
