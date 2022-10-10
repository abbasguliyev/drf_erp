from warehouse.models import Warehouse
from company.models import Office
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Office)
def create_warehouse(sender, instance, created, **kwargs):
    if created:
        office = instance
        company = office.company
        name = f"{office.name} anbarı"
        warehouse = Warehouse.objects.filter(name=name, office=office, company=company)
        if len(warehouse) == 0:
            Warehouse.objects.create(
                name=name,
                office=office,
                company=company
            ).save()