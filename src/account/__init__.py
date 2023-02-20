ACTIV = "Aktiv"
DEACTIV = "Deaktiv"

FIX_COMISSION = 'Fix+Kommissiya'
COMISSION = "Kommissiya"
FIX = "Fix"

HOLDING = "Holding"
COMPANY = "Şirkət"

VIP = "VIP"
STANDART = "Standart"

REGISTER_TYPE_CHOICES = [
    (HOLDING, "Holding"),
    (COMPANY, "Şirkət"),
]

SALARY_STYLE_CHOICES = [
    (FIX_COMISSION, "Fix+Kommissiya"),
    (COMISSION, "Kommissiya"),
    (FIX, "Fix"),
]

CUSTOMER_TYPE_CHOICES = [
    (VIP, "VIP"),
    (STANDART, "Standart"),
]

EMPLOYEE_ACTIVITY_CHOICES = [
    (ACTIV, "Aktiv"),
    (DEACTIV, "Deaktiv"),
]