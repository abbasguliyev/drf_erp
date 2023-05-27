import json
import os
import datetime
from django.contrib.auth import get_user_model, models
from rest_framework.exceptions import ValidationError
from core.settings import BASE_DIR
from account import FIX
from account.models import Customer, EmployeeStatus, Region, EmployeeActivity
from account import (
    COMPANY,
    HOLDING,
    ACTIV,
    DEACTIV
)
from account.api.selectors import user_list, employee_status_list
import pandas as pd
from PIL import Image

from salary.api.utils import (
    send_amount_to_salary_view, 
    get_back_amount_from_salary_view,    
)

from contract import CONTINUING
from contract.api.selectors import contract_list, contract_creditor_list
from services.api.selectors import service_list


User = get_user_model()

def create_employee_activity(*, employee, status) -> EmployeeActivity:
    obj = EmployeeActivity.objects.create(employee=employee, status=status)
    obj.full_clean()
    obj.save()

    return obj

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
    section=None,
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
    fin_code,
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
                {"detail": "Holdinq işçisi qeydiyyatdan keçirildiyi zaman şirkət daxil edilməməlidir."})
        
        if office is not None:
            raise ValidationError(
                {"detail": "Holdinq işçisi qeydiyyatdan keçirildiyi zaman ofis daxil edilməməlidir."})
    if region is None:
        region = Region.objects.filter(region_name="Bakı").last()

    if profile_image is not None:
        im1 = Image.open(photo_ID)
        im2 = Image.open(profile_image)

        if list(im1.getdata()) == list(im2.getdata()):
            raise ValidationError({"detail": "Ş/V və profil şəkli eyni ola bilməz"})
        
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
        section=section,
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
        fin_code=fin_code,
        electronic_signature=electronic_signature,
        register_type=register_type,
        profile_image=profile_image,
    )
    try:
        user.username = f"user-{user.id}"
        user.save()
    except:
        user.username = f"user-1"
        user.save()
    
    standart_status = employee_status_list().filter(status_name= "STANDART").first()
    if employee_status == None:
        user.employee_status = standart_status
    if user_permissions is not None:
        user.user_permissions.set(user_permissions)
    if groups is not None:
        user.groups.set(groups)

    user.set_password(password)
    user.full_clean()
    user.save()

    return user

def update_user(id, **data) -> User:
    """
    User update funksiyası. Əgər sabit əməkhaqqı dəyişilərsə aşağıdakı if şərti işə düşəcək və
    işçinin maaş kartında yekun əməkhaqqı dəyişikliyə uyğun olaraq yenilənəcək
    """
    user = user_list().filter(id=id).last()

    salary = data.get('salary')
    is_active = data.get('is_active')

    if salary is not None:
        difference = 0
        old_salary = user.salary

        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        
        this_month = f"{now.year}-{now.month}-{1}"
        next_m = d + pd.offsets.MonthBegin(1)

        if salary > old_salary:
            difference = salary - old_salary
            send_amount_to_salary_view(user=user, amount=difference, date=this_month)
            try:
                send_amount_to_salary_view(user=user, amount=difference, date=next_m)
            except:
                pass
        elif salary < old_salary:
            difference = old_salary - salary
            get_back_amount_from_salary_view(user=user, amount=difference, date=this_month)
            try:
                get_back_amount_from_salary_view(user=user, amount=difference, date=next_m)
            except:
                pass

    if is_active is not None:
        if user.is_active == False and is_active == True:
            create_employee_activity(employee=user, status=ACTIV)
        elif user.is_active == True and is_active == False:
            create_employee_activity(employee=user, status=DEACTIV)

def delete_user(user):
    user_contracts = contract_creditor_list().filter(creditor=user, contract__contract_status=CONTINUING).count()
    user_services = service_list().filter(service_creditor=user, is_finished=False).count()
    
    if user_contracts > 0 or user_services > 0:
        raise ValidationError({'detail': f"{user_contracts} müqavilədə kreditordur, {user_services} servisdə ustadır. Bu əməkdaş passiv edilməzdən əvvəl 'Ödəniş İzləmə' menyusuna gedərək iştirak etdiyi müqavilə və ya servislərdən çıxarılmalıdır."})
    
    user.is_active = False
    user.dismissal_date = datetime.date.today()
    user.save()
    create_employee_activity(employee=user, status=DEACTIV)

def create_customer(
        *, fullname: str,
        email: str = None,
        phone_number_1: str,
        phone_number_2: str = None,
        phone_number_3: str = None,
        phone_number_4: str = None,
        region,
        address: str,
        fin_code: str,
        photo_ID,
        back_photo_of_ID=None,
        note: str = None,
) -> Customer:
    customer = Customer.objects.create(
        fullname=fullname,
        email=email,
        phone_number_1=phone_number_1,
        phone_number_2=phone_number_2,
        phone_number_3=phone_number_3,
        phone_number_4=phone_number_4,
        region=region,
        address=address,
        fin_code=fin_code,
        photo_ID=photo_ID,
        back_photo_of_ID=back_photo_of_ID,
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