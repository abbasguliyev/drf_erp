from rest_framework.exceptions import ValidationError
from contract.models import ContractCreditor
from contract.api.selectors import contract_creditor_list
from services.api.selectors import service_list

def contract_creditor_create(*, contract, creditor) -> ContractCreditor:
    creditor_contracts = contract_creditor_list().filter(contract=contract)
    if creditor_contracts.count() > 0:
        raise ValidationError({"detail":"Bir müqaviləyə birdən artıq creditor təyin edilə bilməz"})

    services = service_list().filter(contract=contract)

    for service in services:
        service.service_creditor = creditor
        service.save()
    
    obj = ContractCreditor.objects.create(contract=contract, creditor=creditor)
    obj.full_clean()
    obj.save()

    return obj