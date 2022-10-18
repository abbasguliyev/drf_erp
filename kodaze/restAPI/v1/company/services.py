from company.models import Holding, Company
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
    alliance_holding = Holding.objects.filter(name="ALLIANCE").first()
    company_name = name.upper()
    company_qs = Company.objects.filter(name = company_name, holding=alliance_holding).count()
    if company_qs > 0:
        raise ValidationError({"detail": 'Bu ad ilə şirkət artıq əlavə olunub'})
        
    company = Company.objects.create(
        name=company_name,
        address=address,
        phone=phone,
        email=email,
        web_site=web_site,
        holding = alliance_holding
    )
    company.full_clean()
    company.save()

    return company
