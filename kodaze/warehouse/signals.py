from company.models import Office
from django.db.models.signals import post_save
from django.dispatch import receiver
from warehouse.api.services.warehouse_service import warehouse_create
from warehouse.api.selectors import warehouse_list

@receiver(post_save, sender=Office)
def create_warehouse(sender, instance, created, **kwargs):
    if created:
        office = instance
        company = office.company
        name = f"{office.name} anbarı"
        warehouse = warehouse_list().filter(name=name, office=office, company=company)
        if warehouse.count() == 0:
            warehouse_create(name=name, office=office, company=company)