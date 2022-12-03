import json
import os
from account import FIX
from account.models import Customer, EmployeeStatus, Region
from rest_framework.exceptions import ValidationError
from core.settings import BASE_DIR
import datetime
from account import (
    COMPANY,
    HOLDING
)
from account.api.selectors import user_list, employee_status_list, region_list
from django.contrib.auth import get_user_model

from salary.api.utils import (
    send_amount_to_salary_view, 
    get_back_amount_from_salary_view,    
)

User = get_user_model()


def create_user(
        *, fullname: str,
        phone_number_1: str,
        phone_number_2: str = None,
        region=None,
        address: str = None,
        email=None,
        company=None,
        office=None,
        department=None,
        supervisor=None,
        position,
        photo_ID,
        back_photo_of_ID=None,
        driving_license_photo=None,
        employee_status=None,
        commission=None,
        salary_style: str = FIX,
        salary: float = 0,
        note: str = None,
        electronic_signature,
        profile_image=None,
        register_type: str = None,
        user_permissions=None,
        groups=None,
        password: str,
) -> User:
    if register_type == COMPANY:
        if company == None:
            raise ValidationError(
                {"detail": "Şirkət işçisi qeydiyyatdan keçirildiyi zaman şikət mütləq daxil edilməlidir."})
        
        if office == None:
            raise ValidationError(
                {"detail": "Şirkət işçisi qeydiyyatdan keçirildiyi zaman ofis mütləq daxil edilməlidir."})
        
        if position == None:
            raise ValidationError(
                {"detail": "Şirkət işçisi qeydiyyatdan keçirildiyi zaman vəzifə mütləq daxil edilməlidir."})

    if register_type == HOLDING:
        if company is not None:
            raise ValidationError(
                {"detail": "Holdinq işçisi qeydiyyatdan keçirildiyi zaman şikət daxil edilməməlidir"})
        
        if office is not None:
            raise ValidationError(
                {"detail": "Holdinq işçisi qeydiyyatdan keçirildiyi zaman ofis daxil edilməməlidir"})
    if region is None:
        region = Region.objects.filter(region_name="Bakı").last()
        
    user = User.objects.create(
        fullname=fullname,
        phone_number_1=phone_number_1,
        phone_number_2=phone_number_2,
        region=region,
        address=address,
        email=email,
        company=company,
        office=office,
        department=department,
        supervisor=supervisor,
        position=position,
        photo_ID=photo_ID,
        back_photo_of_ID=back_photo_of_ID,
        driving_license_photo=driving_license_photo,
        employee_status=employee_status,
        commission=commission,
        salary_style=salary_style,
        salary=salary,
        note=note,
        electronic_signature=electronic_signature,
        register_type=register_type,
        profile_image=profile_image,
    )

    standart_status = employee_status_list().filter(status_name= "STANDART").first()
    if employee_status == None:
        user.employee_status = standart_status
    if user_permissions is not None:
        user.user_permissions.set(user_permissions)
    if groups is not None:
        user.groups.set(groups)

    try:
        user.username = f"user-{user.id}"
    except:
        user.username = f"user-1"

    user.set_password(password)
    user.full_clean()
    user.save()

    return user

def update_user(id, **data) -> User:
    """
    User update funksiyası. Əgər sabit əməkhaqqı dəyişilərsə aşağıdakı if şərti işə düşəcək və
    işçinin maaş kartında yekun əməkhaqqı dəyişikliyə uyğun olaraq yenilənəcək
    """
    try:
        salary_data = data['salary']
    except:
        salary_data = None

    if salary_data is not None:
        salary = data['salary']
        user = user_list().filter(id=id).last()
        difference = 0
        old_salary = user.salary

        now = datetime.date.today()
        this_month = f"{now.year}-{now.month}-{1}"

        if salary > old_salary:
            difference = salary - old_salary
            send_amount_to_salary_view(user=user, amount=difference, date=this_month)
        elif salary < old_salary:
            difference = old_salary - salary
            get_back_amount_from_salary_view(user=user, amount=difference, date=this_month)

    obj = user_list().filter(id=id).update(**data)
    return obj


def create_customer(
        *, fullname: str,
        email: str = None,
        profile_image=None,
        photo_ID,
        back_photo_of_ID=None,
        phone_number_1: str,
        phone_number_2: str = None,
        phone_number_3: str = None,
        phone_number_4: str = None,
        address: str,
        region,
        note: str = None,
) -> Customer:
    customer = Customer.objects.create(
        fullname=fullname,
        email=email,
        profile_image=profile_image,
        photo_ID=photo_ID,
        back_photo_of_ID=back_photo_of_ID,
        phone_number_1=phone_number_1,
        phone_number_2=phone_number_2,
        phone_number_3=phone_number_3,
        phone_number_4=phone_number_4,
        address=address,
        region=region,
        note=note,
    )
    customer.save()
    return customer


def create_employee_status(*, status_name: str) -> EmployeeStatus:
    statuses = employee_status_list().filter(status_name= status_name.upper()).count()
    if statuses > 0:
        raise ValidationError({"detail": "Eyni adlı statusu 2 dəfə əlavə etmək olmaz!"})
    employee_status = EmployeeStatus.objects.create(status_name=status_name.upper())
    employee_status.save()
    return employee_status


def all_region_create() -> None:
    filename = os.path.join(BASE_DIR, 'cities.json')
    with open(filename) as fp:
        cities = json.load(fp)
    for city in cities:
        regions = region_list().filter(region_name= city['name']).count()
        if regions > 0:
            continue
        region = Region.objects.create(region_name=city['name'])
        region.save()


def region_create(region_name: str) -> Region:
    regions = region_list().filter(region_name= region_name).count()
    if regions > 0:
        raise ValidationError({"detail": "Eyni adlı bölgəni 2 dəfə əlavə etmək olmaz!"})
    region = Region.objects.create(region_name=region_name)
    region.save()
    return region
