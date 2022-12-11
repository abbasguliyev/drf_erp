from company.models import Department, Holding, Company, Office, Position, Section
from rest_framework.exceptions import ValidationError

def holding_create(name: str) -> Holding:
    holding_name = name.upper()
    try:
        holding = Holding.objects.create(name=holding_name)
        holding.full_clean()
        holding.save()
    
        return holding
    except:
        raise ValidationError({"detail": 'Bu ad ilə holding artıq əlavə olunub'})

def company_create(
    *, name: str,
    address: str,
    phone: str,
    email: str,
    web_site: str = None
) -> Company:
    company_name = name.upper()
    company_qs = Company.objects.filter(name = company_name).count()
    if company_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə şirkət artıq əlavə olunub'})
        
    company = Company.objects.create(
        name=company_name,
        address=address,
        phone=phone,
        email=email,
        web_site=web_site,
    )
    company.full_clean()
    company.save()

    return company

def department_create(*, name: str) -> Department:
    department_qs = Department.objects.filter(name = name).count()
    if department_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə departament artıq əlavə olunub'})
        
    department = Department.objects.create(name=name)
    department.full_clean()
    department.save()

    return department

def office_create(*, name: str, company) -> Office:
    office_qs = Office.objects.filter(name = name, company=company).count()
    if office_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə ofis artıq əlavə olunub'})
        
    office = Office.objects.create(name=name, company=company)
    office.full_clean()
    office.save()

    return office

def section_create(*, name: str) -> Section:
    section_qs = Section.objects.filter(name = name).count()
    if section_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə şöbə artıq əlavə olunub'})
        
    section = Section.objects.create(name=name)
    section.full_clean()
    section.save()

    return section

def position_create(*, name:str) -> Position:
    position_name = name.upper()
    position_qs = Position.objects.filter(name = position_name).count()
    if position_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə vəzifə artıq əlavə olunub'})
        
    position = Position.objects.create(name=position_name)
    position.full_clean()
    position.save()

    return position