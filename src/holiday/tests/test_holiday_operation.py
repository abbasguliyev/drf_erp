from django.test import TestCase
from django.contrib.auth import get_user_model
from account import (
    SALARY_STYLE_CHOICES,
    REGISTER_TYPE_CHOICES
)
from company.models import (
    Company,
    Office
)
from holiday.models import HolidayOperation


User = get_user_model()

class HolidayOperationTest(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
