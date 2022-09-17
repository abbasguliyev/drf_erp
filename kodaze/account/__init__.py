MONTHLY = 'aylıq'
DAILY = "günlük"
WEEKLY = "həftəlik"
FIX = "fix"

XIDMETI_MUQAVILE = "xidməti müqavilə"
EMEK_MUQAVILE = "əmək müqaviləsi"

VIP = "VIP"
STANDART = "Standart"

CONTRACT_TYPE_CHOICES = [
    (XIDMETI_MUQAVILE, "xidməti müqavilə"),
    (EMEK_MUQAVILE, "əmək müqaviləsi"),
]

SALARY_STYLE_CHOICES = [
    (MONTHLY, "aylıq"),
    (DAILY, "günlük"),
    (WEEKLY, "həftəlik"),
    (FIX, "fix"),
]


CUSTOMER_TYPE_CHOICES = [
    (VIP, "VIP"),
    (STANDART, "Standart"),
]
