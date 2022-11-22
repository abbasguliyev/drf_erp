import datetime

from core.utils.ocean_contract_pdf_create import (
    ocean_contract_pdf_canvas,
    ocean_create_contract_pdf,
    ocean_installment_contract_pdf_canvas,
    ocean_installment_create_contract_pdf,
)

from core.utils.magnus_contract_pdf_create import (
    magnus_create_contract_pdf,
    magnus_contract_pdf_canvas,
    magnus_installment_create_contract_pdf,
    magnus_installment_contract_pdf_canvas,
)


def create_and_add_pdf_when_contract_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = ocean_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = magnus_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf = contract_pdf
        instance.save()


def create_and_add_pdf_when_contract_installment_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = ocean_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = magnus_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf_elave = contract_pdf
        instance.save()


def pdf_create_when_contract_updated(sender, instance, created):
    create_and_add_pdf_when_contract_updated(
        sender=sender, instance=instance, created=created)
    create_and_add_pdf_when_contract_installment_updated(
        sender=sender, instance=instance, created=created)


# ----------------------------------------------------------------------------------------------------------------------

def reduce_product_from_stock(stock, product_quantity):
    # stock.quantity = stock.quantity - int(product_quantity)
    stock.decrease_stock(int(product_quantity))
    stock.save()
    if stock.quantity == 0:
        stock.delete()
    return stock.quantity


def add_product_to_stock(stock, product_quantity):
    # stock.quantity = stock.quantity + int(product_quantity)
    stock.increase_stock(int(product_quantity))
    stock.save()
    return stock.quantity