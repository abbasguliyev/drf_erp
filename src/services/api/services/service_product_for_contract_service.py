from services.models import ServiceProductForContract
from rest_framework.exceptions import ValidationError
from product.api.selectors import product_list
from services.api.selectors import service_product_for_contract_list


def service_product_for_contract_create(
    *, company, product, service_period: int = 1
) -> ServiceProductForContract:
    obj = ServiceProductForContract.objects.create(
        company=company, service_period=service_period, product=product
    )
    obj.full_clean()
    obj.save()

    return obj

def service_product_for_contract_operation(*, company, product_and_period):
    product_and_period_list_full = product_and_period.split(',')
    product_and_period_list = [x for x in product_and_period_list_full if x != ' ' and x != '']

    for product_and_period in product_and_period_list:
        new_list = product_and_period.split('-')
        product_id = new_list[0]
        period = int(new_list[1])

        product = product_list().filter(pk=product_id).last()
        periodic_products = service_product_for_contract_list().filter(product=product)
        if periodic_products.count() == 0:
            service_product_for_contract_create(company=company, product=product, service_period=period)
        else:
            periodic_product = periodic_products.last()
            periodic_product.product = product
            periodic_product.period = period
            periodic_product.save()
