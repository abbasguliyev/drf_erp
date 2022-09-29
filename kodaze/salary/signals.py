from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import datetime

from account.models import User
from company.models import Position
from .models import Manager2Prim, Manager1PrimNew, SalaryView, OfficeLeaderPrim, GroupLeaderPrimNew
from contract.models import Contract
import traceback
from contract import (
    CASH,
    INSTALLMENT
)

@receiver(post_save, sender=Contract)
def create_prim(sender, instance, created, **kwargs):
    if created:
        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        print(f"{now=}")
        print(f"{next_m=}")
        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        contract_loan_term = instance.loan_term
        contract_payment_style = instance.payment_style

        group_leader = instance.group_leader
        if group_leader is not None:
            group_leader_status = group_leader.employee_status
        else:
            group_leader_status = None

        manager1 = instance.manager1
        if manager1 is not None:
            try:
                manager1_status = manager1.employee_status
                manager1_position = manager1.position.name
            except:
                manager1_status = None
                manager1_position = None    
        else:
            manager1_status = None
            manager1_position = None


        manager2 = instance.manager2
        if manager2 is not None:
            try:
                manager2_status = manager2.employee_status
                manager2_position = manager2.position.name
            except:
                manager2_status = None
                manager2_position = None
        else:
            manager2_status = None
            manager2_position = None

        office = instance.office
        company = instance.company
        # department = instance.group_leader.department
        print(f"{company=}")
        # print(f"{department=}")
        if (office is not None) or (office != ""):
            officeLeaderPosition = Position.objects.get(name__icontains="OFFICE LEADER")
            officeLeaders = User.objects.filter(office=office, position=officeLeaderPosition)

            for officeLeader in officeLeaders:
                officeLeader_status = officeLeader.employee_status
                officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeaderPosition)

                officeLeader_salary_view_this_month = SalaryView.objects.get(employee=officeLeader, date=f"{now.year}-{now.month}-{1}")
                officeLeader_salary_view_novbeti_ay = SalaryView.objects.get(employee=officeLeader, date=f"{next_m.year}-{next_m.month}-{1}")

                officeLeader_salary_view_this_month.sales_quantity = float(officeLeader_salary_view_this_month.sale_quantity) + float(instance.product_quantity)
                officeLeader_salary_view_this_month.sales_amount = float(officeLeader_salary_view_this_month.sales_amount) + (float(instance.product.price) * float(instance.product_quantity))
                officeLeader_salary_view_this_month.save()

                officeLeader_salary_view_novbeti_ay.final_salary = float(officeLeader_salary_view_novbeti_ay.final_salary) + (float(officeleader_prim.prim_for_office) * float(instance.product_quantity))
                officeLeader_salary_view_novbeti_ay.save()

        # --------------------------------------------------------
        if (group_leader_status is not None):
            """
            GroupLeaderin yeni uslubla salary hesablanmasi
            """
            group_leader_prim = GroupLeaderPrimNew.objects.get(prim_status=group_leader_status, position=group_leader.position)
            
            group_leader_salary_view_this_month = SalaryView.objects.get(employee=group_leader, date=f"{now.year}-{now.month}-{1}")
            group_leader_salary_view_novbeti_ay = SalaryView.objects.get(employee=group_leader, date=next_m)

            group_leader_salary_view_this_month.sales_quantity = float(group_leader_salary_view_this_month.sale_quantity) + float(instance.product_quantity)
            group_leader_salary_view_this_month.sales_amount = float(group_leader_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            
            group_leader_salary_view_this_month.save()
            if contract_payment_style == CASH:
                group_leader_salary_view_novbeti_ay.final_salary = float(group_leader_salary_view_novbeti_ay.final_salary) + (float(group_leader_prim.cash) * float(instance.product_quantity))
            elif contract_payment_style == INSTALLMENT:
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    group_leader_salary_view_novbeti_ay.final_salary = float(group_leader_salary_view_novbeti_ay.final_salary) + (float(group_leader_prim.cash) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    group_leader_salary_view_novbeti_ay.final_salary = float(group_leader_salary_view_novbeti_ay.final_salary) + (float(group_leader_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    group_leader_salary_view_novbeti_ay.final_salary = float(group_leader_salary_view_novbeti_ay.final_salary) + (float(group_leader_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    group_leader_salary_view_novbeti_ay.final_salary = float(group_leader_salary_view_novbeti_ay.final_salary) + (float(group_leader_prim.installment_19_24) * float(instance.product_quantity))

            group_leader_salary_view_novbeti_ay.save()
        
        # --------------------------------------------------------
        if (manager1_position == "DEALER"):
            """
            Manager1in yeni uslubla salary hesablanmasi
            """
            manager1_prim = Manager1PrimNew.objects.get(prim_status=manager1_status, position=manager1.position)
            
            manager1_salary_view_this_month = SalaryView.objects.get(employee=manager1, date=f"{now.year}-{now.month}-{1}")
            manager1_salary_view_novbeti_ay = SalaryView.objects.get(employee=manager1, date=next_m)

            manager1_salary_view_this_month.sales_quantity = float(manager1_salary_view_this_month.sale_quantity) + float(instance.product_quantity)
            manager1_salary_view_this_month.sales_amount = float(manager1_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))

            manager1_salary_view_this_month.save()

            if contract_payment_style == CASH:
                manager1_salary_view_novbeti_ay.final_salary = float(manager1_salary_view_novbeti_ay.final_salary) + (float(manager1_prim.cash) * float(instance.product_quantity))
            elif contract_payment_style == INSTALLMENT:
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    manager1_salary_view_novbeti_ay.final_salary = float(manager1_salary_view_novbeti_ay.final_salary) + (float(manager1_prim.cash) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    manager1_salary_view_novbeti_ay.final_salary = float(manager1_salary_view_novbeti_ay.final_salary) + (float(manager1_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    manager1_salary_view_novbeti_ay.final_salary = float(manager1_salary_view_novbeti_ay.final_salary) + (float(manager1_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    manager1_salary_view_novbeti_ay.final_salary = float(manager1_salary_view_novbeti_ay.final_salary) + (float(manager1_prim.installment_19_24) * float(instance.product_quantity))
            manager1_salary_view_novbeti_ay.save()

        # --------------------------------------------------------
        if (manager2_position == "CANVASSER"):
            manager2_prim = Manager2Prim.objects.get(prim_status=manager2_status, position=manager2.position)

            manager2_salary_view_this_month = SalaryView.objects.get(employee=manager2, date=f"{now.year}-{now.month}-{1}")
            manager2_salary_view_novbeti_ay = SalaryView.objects.get(employee=manager2, date=next_m)

            manager2_salary_view_this_month.sales_quantity = float(manager2_salary_view_this_month.sale_quantity) + float(instance.product_quantity)
            manager2_salary_view_this_month.sales_amount = float(manager2_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            manager2_salary_view_this_month.save()

            prim_for_sales_quantity = 0
            
            if (manager2_salary_view_this_month.sales_quantity >= 9) and (manager2_salary_view_this_month.sales_quantity <= 14):
                prim_for_sales_quantity = manager2_prim.sale_9_14
            elif (manager2_salary_view_this_month.sales_quantity >= 15):
                prim_for_sales_quantity = manager2_prim.sale_15p
            elif (manager2_salary_view_this_month.sales_quantity >= 20):
                prim_for_sales_quantity = manager2_prim.sale_20p

            manager2_salary_view_novbeti_ay.final_salary = float(manager2_salary_view_novbeti_ay.final_salary) + (float(manager2_prim.prim_for_team) * float(instance.product_quantity)) + float(prim_for_sales_quantity)

            manager2_salary_view_novbeti_ay.save()

        
        manager2Position = Position.objects.get(name__icontains="CANVASSER")
        manager2s = User.objects.filter(office=office, position=manager2Position)

        for manager2 in manager2s:
            manager2_status = manager2.employee_status
            manager2_prim = Manager2Prim.objects.get(prim_status=manager2_status, position=manager2.position)

            manager2_salary_view_novbeti_ay = SalaryView.objects.get(employee=manager2, date=next_m)

            manager2_salary_view_novbeti_ay.final_salary = float(manager2_salary_view_novbeti_ay.final_salary) + (float(manager2_prim.prim_for_office) * float(instance.product_quantity))

            manager2_salary_view_novbeti_ay.save()