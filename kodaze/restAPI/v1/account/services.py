from datetime import date
import json
import os
from django.contrib.auth import get_user_model
from account import MONTHLY
from account.models import Customer, EmployeeStatus, Region
from rest_framework.exceptions import ValidationError
from core.settings import BASE_DIR

User = get_user_model()

def create_user(
    *, email = None,
    fullname: str,
    start_date_of_work: date = date.today(),
    dismissal_date: date = None,
    phone_number_1: str,
    phone_number_2: str = None,
    photo_ID,
    back_photo_of_ID = None,
    driving_license_photo = None,
    department = None,
    company = None,
    office = None,
    section = None,
    position = None,
    team = None,
    employee_status = None,
    salary_style: str = MONTHLY,
    contract_type: str = None,
    salary: float = 0,
    note: str = None,
    profile_image = None,
    supervisor = None,
    user_permissions = None,
    groups = None,
    password: str,
) -> User:
    user = User.objects.create(
        email = email,
        fullname = fullname,
        start_date_of_work= start_date_of_work,
        dismissal_date = dismissal_date,
        phone_number_1 = phone_number_1,
        phone_number_2 = phone_number_2,
        photo_ID = photo_ID,
        back_photo_of_ID = back_photo_of_ID,
        driving_license_photo = driving_license_photo,
        department = department,
        company = company,
        office = office,
        section = section,
        position = position,
        team = team,
        employee_status = employee_status,
        salary_style = salary_style,
        contract_type = contract_type,
        salary = salary,
        note = note,
        profile_image = profile_image,
        supervisor = supervisor,
    )
    standart_status = EmployeeStatus.objects.filter(status_name="STANDART").first()
    if employee_status == None:
        user.employee_status = standart_status
    if user_permissions is not None:
        user.user_permissions.set(user_permissions)
    if groups is not None:
        user.groups.set(groups)
    last_user_id = User.objects.all().values_list('id', flat=True).last()
    try:
        user.username = f"user-{last_user_id+1}"
    except:
        user.username = f"user-1"
    user.set_password(password)
    user.full_clean()
    user.save()

    return user

def create_customer(
    *, fullname: str,
    email: str = None,
    profile_image = None,
    photo_ID,
    back_photo_of_ID = None,
    phone_number_1: str,
    phone_number_2: str = None,
    phone_number_3: str = None,
    phone_number_4: str = None,
    address: str, 
    region,
    note: str = None,
) -> Customer:
    customer = Customer.objects.create(
        fullname = fullname,
        email = email,
        profile_image = profile_image,
        photo_ID = photo_ID,
        back_photo_of_ID = back_photo_of_ID,
        phone_number_1 = phone_number_1,
        phone_number_2 = phone_number_2,
        phone_number_3 = phone_number_3,
        phone_number_4 = phone_number_4,
        address = address,
        region = region,
        note = note,
    )
    customer.save()
    return customer

def create_employee_status(*, status_name: str) -> EmployeeStatus:
    statuses = EmployeeStatus.objects.filter(status_name=status_name.upper()).count()
    if statuses>0:
        raise ValidationError({"detail": "Eyni adlı statusu 2 dəfə əlavə etmək olmaz!"})
    employee_status = EmployeeStatus.objects.create(status_name = status_name.upper())
    employee_status.save()
    return employee_status

def all_region_create() -> None:
    filename = os.path.join(BASE_DIR, 'cities.json')
    with open(filename) as fp:
        cities = json.load(fp)
    for city in cities:
        regions = Region.objects.filter(region_name=city['name']).count()
        if regions>0:
            continue
        region = Region.objects.create(region_name=city['name'])
        region.save()

def region_create(region_name: str) -> Region:
    regions = Region.objects.filter(region_name=region_name).count()
    if regions>0:
        raise ValidationError({"detail": "Eyni adlı bölgəni 2 dəfə əlavə etmək olmaz!"})
    region = Region.objects.create(region_name=region_name)
    region.save()
    return region