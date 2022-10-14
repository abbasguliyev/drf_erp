from contract.models import Contract
from . models import Service, ServicePayment
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd
from django.db import transaction

from .tasks import create_services_task


@receiver(post_save, sender=Contract)
def create_services(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: create_services_task.delay(instance.id))


@receiver(post_save, sender=Service)
def create_service_payment(sender, instance, created, **kwargs):
    if created:
        loan_term = instance.loan_term
        installment = instance.installment
        if int(loan_term) == 0:
            loan_term = 1
        print(f"****************************{loan_term=}")
        print(f"****************************{installment=}")
        discount = instance.discount
        if discount == None:
            discount = 0

        initial_payment = instance.initial_payment
        if initial_payment == None:
            initial_payment = 0

        price = instance.price
        total = float(price) - float(initial_payment) - float(discount)
        result1 = total // loan_term
        result2 = result1 * (loan_term - 1)
        last_month = total - result2
        # now_d = service_date
        # now = f"{now_d.year}-{now_d.month}-{1}"

        now_d = instance.create_date
        service_date_str = instance.service_date
        print(f"{service_date_str=}")

        # service_date = pd.to_datetime(f"{service_date_str.year}-{service_date_str.month}-{service_date_str.day}")
        try:
            service_date = datetime.datetime.strptime(
                f"{service_date_str.day}-{service_date_str.month}-{service_date_str.year}", '%d-%m-%Y')
        except:
            # service_date = datetime.datetime.strptime(service_date_str, '%d-%m-%Y')
            service_date = service_date_str
        inc_month = pd.date_range(service_date, periods=loan_term+1, freq='M')

        if installment == False:
            service_payment = ServicePayment.objects.create(
                service=instance,
                total_amount_to_be_paid=total,
                amount_to_be_paid=last_month,
                payment_date=f"{service_date.year}-{service_date.month}-{service_date.day}"
            ).save()
        elif installment == True:
            j = 1
            while(j <= int(loan_term)):
                if(j == int(loan_term)):
                    if(service_date.day < 29):
                        service_payment = ServicePayment.objects.create(
                            service=instance,
                            total_amount_to_be_paid=total,
                            amount_to_be_paid=last_month,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                        ).save()
                    elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                        if(inc_month[j].day <= service_date.day):
                            service_payment = ServicePayment.objects.create(
                                service=instance,
                                total_amount_to_be_paid=total,
                                amount_to_be_paid=last_month,
                                payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                            ).save()
                        elif(inc_month[j].day > service_date.day):
                            service_payment = ServicePayment.objects.create(
                                service=instance,
                                total_amount_to_be_paid=total,
                                amount_to_be_paid=last_month,
                                payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                            ).save()
                else:
                    if(service_date.day < 29):
                        service_payment = ServicePayment.objects.create(
                            service=instance,
                            total_amount_to_be_paid=total,
                            amount_to_be_paid=result1,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                        ).save()
                    elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                        if(inc_month[j].day <= service_date.day):
                            service_payment = ServicePayment.objects.create(
                                service=instance,
                                total_amount_to_be_paid=total,
                                amount_to_be_paid=result1,
                                payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                            ).save()
                        elif(inc_month[j].day > service_date.day):
                            service_payment = ServicePayment.objects.create(
                                service=instance,
                                total_amount_to_be_paid=total,
                                amount_to_be_paid=result1,
                                payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                            ).save()
                j += 1