import datetime
import traceback
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from salary.models import SalaryDeduction, SalaryView
from account.models import User
from holiday.api.serializers import (
    HoldingExceptionWorkerSerializer,
    EmployeeWorkingDaySerializer,
    HoldingWorkingDaySerializer,
    TeamWorkingDaySerializer,
    TeamExceptionWorkerSerializer, 
    OfficeWorkingDaySerializer,
    OfficeExceptionWorkerSerializer,
    CompanyWorkingDaySerializer,
    CompanyExceptionWorkerSerializer,
    SectionWorkingDaySerializer,
    SectionExceptionWorkerSerializer,
    PositionWorkingDaySerializer,
    PositionExceptionWorkerSerializer
)
from holiday.models import (
    EmployeeWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    SectionWorkingDay,
    PositionWorkingDay
)
from account.api.selectors import user_list
from salary.api.selectors import salary_view_list

# --------------------------------------------------------------------------------------------------------------------------

def company_employee_tetil_hesablama(company, company_name, date, holidays, working_days_count, non_working_days_count, exception_workers=list()):
    """
    Bu method holding, company, office, section, team ve position-nin is ve qeyri is working_dayi hesablanan zaman onlarla elaqeli olan
    employeelerin is ve qeyri is working_dayini hesablamaq ucundur. Hemcinin eger holding-in is ve qeyri is working_dayi hesablanirsa bu zaman yuxarida
    sadaladigim diger obyektlerinde is ve qeyri is working_dayi uygun olaraq deyisir.
    """
    if(company=="holding"):
        employeeler = list(user_list())
        office_working_day = OfficeWorkingDay.objects.filter(date=date)
        for o in office_working_day:
            o.working_days_count = working_days_count
            o.non_working_days_count = non_working_days_count
            o.holidays = holidays
            o.save()
        company_working_day = CompanyWorkingDay.objects.filter(date=date)
        for s in company_working_day:
            s.working_days_count = working_days_count
            s.non_working_days_count = non_working_days_count
            s.holidays = holidays
            s.save()
        section_working_day = SectionWorkingDay.objects.filter(date=date)
        for sh in section_working_day:
            sh.working_days_count = working_days_count
            sh.non_working_days_count = non_working_days_count
            sh.holidays = holidays
            sh.save()
        position_working_day = PositionWorkingDay.objects.filter(date=date)
        for v in position_working_day:
            v.working_days_count = working_days_count
            v.non_working_days_count = non_working_days_count
            v.holidays = holidays
            v.save()
        team_working_day = TeamWorkingDay.objects.filter(date=date)
        for k in team_working_day:
            k.working_days_count = working_days_count
            k.non_working_days_count = non_working_days_count
            k.holidays = holidays
            k.save()
    elif(company=="company"):
        employeeler = list(user_list(filters={'company': company_name}))
    elif(company=="section"):
        employeeler = list(user_list(filters={'section': company_name}))
    elif(company=="office"):
        employeeler = list(user_list(filters={'office': company_name}))
    elif(company=="team"):
        employeeler = list(user_list(filters={'team': company_name}))
    elif(company=="position"):
        employeeler = list(user_list(filters={'position': company_name}))

    z = 1
    for employee in employeeler:
        if exception_workers != list():
            if employee in exception_workers:
                continue
        try:
            employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
            employee_working_day.holidays = holidays
            employee_working_day.working_days_count = working_days_count
            employee_working_day.non_working_days_count = non_working_days_count
            employee_working_day.save()
        except:
            traceback.print_exc()
        z+=1
    return True

def instisna_employee_create(serializer, company, company_name, obj_working_day):
    date = obj_working_day.date
    obj_working_day_holidays = obj_working_day.holidays
    date_list = []
    k_date_list = []
    
    holidays = serializer.validated_data.get("holidays")
    holidays_l = holidays.rstrip("]").lstrip("[").split(",")
    for i in holidays_l:
        new_el = i.strip().strip("'").strip('"')
        date_list.append(new_el)

    exception_workers = serializer.validated_data.get("exception_workers")

    # now = datetime.date.today()

    # d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    # next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{date.year}-{date.month}-{1}").days_in_month

    for employee in exception_workers:
        employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
        if employee_working_day.holidays is not None:
            employee_working_day_holidays = obj_working_day_holidays.rstrip("]").lstrip("[").split(",")
            for i in employee_working_day_holidays:
                new_el = i.strip().strip("'").strip('"')
                k_date_list.append(new_el)

            for i in date_list:
                if i in k_date_list:
                    k_date_list.remove(i)
        employee_working_day.holidays = k_date_list
        employee_working_day.working_days_count = float(days_in_mont) - len(k_date_list)
        employee_working_day.non_working_days_count = len(k_date_list)
        employee_working_day.save()

    serializer.save(holidays=date_list, exception_workers=exception_workers)

def exception_worker_update(serializer, company, company_name, obj_working_day, obj_exception_worker):
    date = obj_working_day.date
    obj_working_day_holidays = obj_working_day.holidays

    date_list = []
    k_date_list = []
    q_date_list = []

    k_holidays = obj_exception_worker.holidays
    k_holidays_l = k_holidays.rstrip("]").lstrip("[").split(",")
    for i in k_holidays_l:
        new_el = i.strip().strip("'").strip('"')
        k_date_list.append(new_el)

    # now = datetime.date.today()

    # d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    # next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{date.year}-{date.month}-{1}").days_in_month

    holidays = serializer.validated_data.get("holidays")
    if holidays == None:
        holidays = k_date_list
        holidays_l = holidays
        date_list = k_date_list
    else:
        holidays_l = holidays.rstrip("]").lstrip("[").split(",")
        for i in holidays_l:
            new_el = i.strip().strip("'").strip('"')
            date_list.append(new_el)

    u_exception_workers = []

    exception_workers = serializer.validated_data.get("exception_workers")
    if exception_workers == None:
        exception_workers = list(obj_exception_worker.exception_workers.all())

    k_exception_workers = list(obj_exception_worker.exception_workers.all())

    for i in k_exception_workers:
        u_exception_workers.append(i)

    for j in exception_workers:
        if j in u_exception_workers:
            continue
        else:
            u_exception_workers.append(j)

    if (
        (serializer.validated_data.get("exception_workers") == None or serializer.validated_data.get("exception_workers") == "") 
        and 
        (serializer.validated_data.get("holidays") != None)
    ):
        for employee in u_exception_workers:
            employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
            if employee_working_day.holidays is not None:
                employee_working_day_holidays = obj_working_day_holidays.rstrip("]").lstrip("[").split(",")
                for i in employee_working_day_holidays:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                if len(date_list) == len(q_date_list):
                    employee_working_day.holidays = list(q_date_list)
                    employee_working_day.working_days_count = float(days_in_mont)
                    employee_working_day.non_working_days_count = 0
                    employee_working_day.save()
                else:
                    for i in date_list:
                        if i in q_date_list:
                            q_date_list.remove(i)
                        employee_working_day.holidays = list(q_date_list)
                        employee_working_day.working_days_count = float(days_in_mont) - len(date_list)
                        employee_working_day.non_working_days_count = len(date_list)
                        employee_working_day.save()
    elif(
        (serializer.validated_data.get("exception_workers") != None) 
        and 
        (serializer.validated_data.get("holidays") == None)
    ):
        for employee in exception_workers:
            employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
            if employee_working_day.holidays is not None:
                employee_working_day_holidays = obj_working_day_holidays.rstrip("]").lstrip("[").split(",")
                for i in employee_working_day_holidays:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                for i in date_list:
                    if i in q_date_list:
                        q_date_list.remove(i)
            employee_working_day.holidays = list(q_date_list)
            employee_working_day.working_days_count = float(days_in_mont) - len(date_list)
            employee_working_day.non_working_days_count = len(date_list)
            employee_working_day.save()
    elif(
        (serializer.validated_data.get("exception_workers") != None) 
        and 
        (serializer.validated_data.get("holidays") != None)
    ):
        for employee in u_exception_workers:
            employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
            if employee_working_day.holidays is not None:
                employee_working_day_holidays = obj_working_day_holidays.rstrip("]").lstrip("[").split(",")
                for i in employee_working_day_holidays:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                if len(date_list) == len(q_date_list):
                    employee_working_day.holidays = list(q_date_list)
                    employee_working_day.working_days_count = float(days_in_mont)
                    employee_working_day.non_working_days_count = 0
                    employee_working_day.save()
                else:
                    for i in date_list:
                        if i in q_date_list:
                            q_date_list.remove(i)
                        employee_working_day.holidays = list(q_date_list)
                        employee_working_day.working_days_count = float(days_in_mont) - len(date_list)
                        employee_working_day.non_working_days_count = len(date_list)
                        employee_working_day.save()

    # serializer.save(holidays=date_list, exception_workers=u_exception_workers)
    serializer.save()

def exception_worker_delete(obj_working_day, obj_exception_worker):
    exception_workers = obj_exception_worker.exception_workers.all()

    date = obj_working_day.date

    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    for employee in exception_workers:
        employee_working_day = EmployeeWorkingDay.objects.get(employee=employee, date=date)
        if employee_working_day.holidays is not None: 
            employee_working_day.holidays = None
            employee_working_day.working_days_count = float(days_in_mont)
            employee_working_day.non_working_days_count = 0
            employee_working_day.save()


def employee_holidays_calc(serializer, obj):
    date_list = []
    odenisli_icaze_date_list = []
    odenissiz_icaze_date_list = []

    employee = obj.employee

    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holidays = serializer.validated_data.get("holidays")
    if holidays is not None:
        holidays_l = holidays.rstrip("]").lstrip("[").split(",")
    else:
        holidays_l = []
        
    for i in holidays_l:
        new_el = i.strip().strip("'").strip('"')
        date_list.append(new_el)

    paid_leave_days = serializer.validated_data.get("paid_leave_days")
    unpaid_leave_days = serializer.validated_data.get("unpaid_leave_days")

    if paid_leave_days is not None:
        paid_leave_days_l = paid_leave_days.rstrip("]").lstrip("[").split(",")
    else:
        paid_leave_days_l = []

    if unpaid_leave_days is not None:
        unpaid_leave_days_l = unpaid_leave_days.rstrip("]").lstrip("[").split(",")
    else:
        unpaid_leave_days_l = []

    for i in paid_leave_days_l:
        new_elm = i.strip().strip("'").strip('"')
        odenisli_icaze_date_list.append(new_elm)

    for i in unpaid_leave_days_l:
        new_elm1 = i.strip().strip("'").strip('"')
        odenissiz_icaze_date_list.append(new_elm1)

    k_qeyri_working_days = obj.non_working_days_count

    non_working_days_count = float(len(date_list)) + float(len(odenisli_icaze_date_list)) + float(len(odenissiz_icaze_date_list))
    working_days_count = float(days_in_mont)
    working_days_count = float(working_days_count) - float(non_working_days_count)

    is_paid = serializer.validated_data.get("is_paid")
    payment_amount = serializer.validated_data.get("payment_amount")

    if is_paid == True:
        try:
            salary_goruntulenme = salary_view_list(filters={'employee': employee, 'date': d}).last()
            salary_goruntulenme.final_salary = float(salary_goruntulenme.final_salary) - float(payment_amount)
            salary_goruntulenme.save()
            salarydeduction = SalaryDeduction.objects.create(employee=employee, amount=payment_amount, note="ödənişli icazə ilə əlaqədar", date=now)
            salarydeduction.save()
        except:
            return Response({"detail": "Maaş kartında xəta"}, status=status.HTTP_400_BAD_REQUEST)

    # serializer.save(holidays=date_list, working_days_count=working_days_count, non_working_days_count=non_working_days_count)
    serializer.save( working_days_count=working_days_count, non_working_days_count=non_working_days_count)
    return True

def employee_holidays_delete(obj_working_day):
    
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    obj_working_day.holidays = None
    obj_working_day.paid_leave_days = None
    obj_working_day.unpaid_leave_days = None
    obj_working_day.working_days_count = float(days_in_mont)
    obj_working_day.non_working_days_count = 0
    obj_working_day.save()
    

def working_day_update(serializer, company, company_name, obj_working_day):
    date = obj_working_day.date
    working_days_count = obj_working_day.working_days_count
    non_working_days_count = obj_working_day.non_working_days_count
    date_list = []
    k_date_list = []
    u_date_list = []

    k_holidays = obj_working_day.holidays
    if k_holidays is not None:
        k_holidays_l = k_holidays.rstrip("]").lstrip("[").split(",")
        for i in k_holidays_l:
            new_el = i.strip().strip("'").strip('"')
            k_date_list.append(new_el)
    else:
        k_date_list = []

    holidays = serializer.validated_data.get("holidays")
    if holidays == None:
        holidays = k_date_list
        holidays_l = holidays
    else:
        holidays_l = holidays.rstrip("]").lstrip("[").split(",")
        for i in holidays_l:
            new_el = i.strip().strip("'").strip('"')
            date_list.append(new_el)

    # for i in date_list:
    #     u_date_list.append(i)

    # for j in k_date_list:
    #     if j in u_date_list:
    #         continue
    #     else:
    #         u_date_list.append(j)
    k_qeyri_working_days = obj_working_day.non_working_days_count
    non_working_days_count = len(date_list)
    k_working_days_count = obj_working_day.working_days_count
    working_days_count = float(k_working_days_count) - (float(non_working_days_count) - float(k_qeyri_working_days))
    company_employee_tetil_hesablama(
        company=company, 
        company_name=company_name, 
        date=date, 
        holidays=date_list, 
        working_days_count=working_days_count, 
        non_working_days_count=non_working_days_count
    )

    serializer.save(
        non_working_days_count = non_working_days_count, 
        working_days_count = working_days_count,
        holidays=date_list
    )

# --------------------------------------------------------------------------------------------------------------------------

def holding_working_day_update(self, request, *args, **kwargs):
    holding_working_day = self.get_object()
    serializer = HoldingWorkingDaySerializer(holding_working_day, data=request.data, partial=True)
    try:
        if serializer.is_valid():
            working_day_update(serializer=serializer, company="holding", company_name=holding_working_day.holding, obj_working_day=holding_working_day)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)


def holding_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        holding_working_day = serializer.validated_data.get("working_day")
        instisna_employee_create(serializer=serializer, company="holding", company_name=holding_working_day.holding, obj_working_day=holding_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def holding_exception_worker_working_day_update(self, request, *args, **kwargs):
    holding_exception_worker_obj = self.get_object()
    serializer = HoldingExceptionWorkerSerializer(holding_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        
        exception_worker_update(serializer=serializer, company="holding", company_name=holding_exception_worker_obj.working_day.holding, obj_working_day=holding_exception_worker_obj.working_day, obj_exception_worker=holding_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def holding_exception_worker_working_day_delete(self, request, *args, **kwargs):
    holding_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=holding_exception_worker_obj.working_day, 
            obj_exception_worker=holding_exception_worker_obj
        )
        holding_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def office_working_day_update(self, request, *args, **kwargs):
    office_working_day = self.get_object()
    serializer = OfficeWorkingDaySerializer(office_working_day, data=request.data, partial=True)

    if serializer.is_valid():
        working_day_update(serializer=serializer, company="office", company_name=office_working_day.office, obj_working_day=office_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def office_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        office_working_day = serializer.validated_data.get("working_day")
        instisna_employee_create(serializer=serializer, company="office", company_name=office_working_day.office, obj_working_day=office_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def office_exception_worker_working_day_update(self, request, *args, **kwargs):
    office_exception_worker_obj = self.get_object()
    serializer = OfficeExceptionWorkerSerializer(office_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        exception_worker_update(serializer=serializer, company="office", company_name=office_exception_worker_obj.working_day.office, obj_working_day=office_exception_worker_obj.working_day, obj_exception_worker=office_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def office_exception_worker_working_day_delete(self, request, *args, **kwargs):
    office_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=office_exception_worker_obj.working_day, 
            obj_exception_worker=office_exception_worker_obj
        )
        office_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def company_working_day_update(self, request, *args, **kwargs):
    company_working_day = self.get_object()
    serializer = CompanyWorkingDaySerializer(company_working_day, data=request.data, partial=True)

    if serializer.is_valid():
        working_day_update(serializer=serializer, company="company", company_name=company_working_day.company, obj_working_day=company_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def company_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        company_working_day = serializer.validated_data.get("working_day")
        instisna_employee_create(serializer=serializer, company="company", company_name=company_working_day.company, obj_working_day=company_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def company_exception_worker_working_day_update(self, request, *args, **kwargs):
    company_exception_worker_obj = self.get_object()
    serializer = CompanyExceptionWorkerSerializer(company_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        exception_worker_update(serializer=serializer, company="company", company_name=company_exception_worker_obj.working_day.company, obj_working_day=company_exception_worker_obj.working_day, obj_exception_worker=company_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def company_exception_worker_working_day_delete(self, request, *args, **kwargs):
    company_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=company_exception_worker_obj.working_day, 
            obj_exception_worker=company_exception_worker_obj
        )
        company_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def section_working_day_update(self, request, *args, **kwargs):
    section_working_day = self.get_object()
    serializer = SectionWorkingDaySerializer(section_working_day, data=request.data, partial=True)

    if serializer.is_valid():
        working_day_update(serializer=serializer, company="section", company_name=section_working_day.section, obj_working_day=section_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def section_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        section_working_day = serializer.validated_data.get("working_day")
        instisna_employee_create(serializer=serializer, company="section", company_name=section_working_day.section, obj_working_day=section_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def section_exception_worker_working_day_update(self, request, *args, **kwargs):
    section_exception_worker_obj = self.get_object()
    serializer = SectionExceptionWorkerSerializer(section_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        exception_worker_update(serializer=serializer, company="section", company_name=section_exception_worker_obj.working_day.section, obj_working_day=section_exception_worker_obj.working_day, obj_exception_worker=section_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def section_exception_worker_working_day_delete(self, request, *args, **kwargs):
    section_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=section_exception_worker_obj.working_day, 
            obj_exception_worker=section_exception_worker_obj
        )
        section_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
# ------------------------------------------------------------------------------------------------

def team_working_day_update(self, request, *args, **kwargs):
    team_working_day = self.get_object()
    serializer = TeamWorkingDaySerializer(team_working_day, data=request.data, partial=True)
    if serializer.is_valid():
        working_day_update(serializer=serializer, company="team", company_name=team_working_day.team, obj_working_day=team_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def team_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        team_working_day = serializer.validated_data.get("team_working_day")
        instisna_employee_create(serializer=serializer, company="team", company_name=team_working_day.team, obj_working_day=team_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def team_exception_worker_working_day_update(self, request, *args, **kwargs):
    team_exception_worker_obj = self.get_object()
    serializer = TeamExceptionWorkerSerializer(team_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        exception_worker_update(serializer=serializer, company="team", company_name=team_exception_worker_obj.working_day.team, obj_working_day=team_exception_worker_obj.working_day, obj_exception_worker=team_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def team_exception_worker_working_day_delete(self, request, *args, **kwargs):
    team_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=team_exception_worker_obj.working_day, 
            obj_exception_worker=team_exception_worker_obj
        )
        team_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def position_working_day_update(self, request, *args, **kwargs):
    position_working_day = self.get_object()
    serializer = PositionWorkingDaySerializer(position_working_day, data=request.data, partial=True)
    if serializer.is_valid():
        working_day_update(serializer=serializer, company="position", company_name=position_working_day.position, obj_working_day=position_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def position_exception_worker_working_day_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        position_working_day = serializer.validated_data.get("working_day")
        instisna_employee_create(serializer=serializer, company="position", company_name=position_working_day.position, obj_working_day=position_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def position_exception_worker_working_day_update(self, request, *args, **kwargs):
    position_exception_worker_obj = self.get_object()
    serializer = PositionExceptionWorkerSerializer(position_exception_worker_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        exception_worker_update(serializer=serializer, company="position", company_name=position_exception_worker_obj.working_day.position, obj_working_day=position_exception_worker_obj.working_day, obj_exception_worker=position_exception_worker_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
    
def position_exception_worker_working_day_delete(self, request, *args, **kwargs):
    position_exception_worker_obj = self.get_object()
    try:
        exception_worker_delete(
            obj_working_day=position_exception_worker_obj.working_day, 
            obj_exception_worker=position_exception_worker_obj
        )
        position_exception_worker_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
# ------------------------------------------------------------------------------------------------

def user_working_day_update(self, request, *args, **kwargs):
    user_working_day = self.get_object()
    serializer = EmployeeWorkingDaySerializer(user_working_day, data=request.data, partial=True)
    if serializer.is_valid():
        employee_holidays_calc(serializer, user_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def user_working_day_patch(self, request, *args, **kwargs):
    user_working_day = self.get_object()
    serializer = EmployeeWorkingDaySerializer(user_working_day, data=request.data, partial=True)
    if serializer.is_valid():
        employee_holidays_calc(serializer, user_working_day)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def user_working_day_delete(self, request, *args, **kwargs):
    user_working_day = self.get_object()
    try:
        employee_holidays_delete(
            obj_working_day=user_working_day
        )
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------


