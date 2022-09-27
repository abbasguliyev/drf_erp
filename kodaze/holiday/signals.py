from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

import datetime
from company.models import Holding, Team, Office, Company, Section, Position
from .models import (
    HoldingWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    SectionWorkingDay,
    PositionWorkingDay
)

# Holding working_day ---------------------------------------------------


@receiver(post_save, sender=Holding)
def holding_working_day_create(sender, instance, created, **kwargs):
    if created:
        holding = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        holding_working_day = HoldingWorkingDay.objects.select_related("holding").filter(
            holding=holding,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(holding_working_day) == 0:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding=holding,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_working_day.save()

        holding_working_day = HoldingWorkingDay.objects.select_related("holding").filter(
            holding=holding,
            date__year=now.year,
            date__month=now.month
        )
        if len(holding_working_day) == 0:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding=holding,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            holding_working_day.save()

# Company working_day ---------------------------------------------------


@receiver(post_save, sender=Company)
def company_working_day_create(sender, instance, created, **kwargs):
    if created:
        company = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        company_working_day = CompanyWorkingDay.objects.select_related("company").filter(
            company=company,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(company_working_day) == 0:
            company_working_day = CompanyWorkingDay.objects.create(
                company=company,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            company_working_day.save()

        company_working_day = CompanyWorkingDay.objects.select_related("company").filter(
            company=company,
            date__year=now.year,
            date__month=now.month
        )
        if len(company_working_day) == 0:
            company_working_day = CompanyWorkingDay.objects.create(
                company=company,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            company_working_day.save()

# Office working_day ---------------------------------------------------


@receiver(post_save, sender=Office)
def office_working_day_create(sender, instance, created, **kwargs):
    if created:
        office = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        office_working_day = OfficeWorkingDay.objects.select_related("office").filter(
            office=office,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(office_working_day) == 0:
            office_working_day = OfficeWorkingDay.objects.create(
                office=office,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            office_working_day.save()

        office_working_day = OfficeWorkingDay.objects.select_related("office").filter(
            office=office,
            date__year=now.year,
            date__month=now.month
        )
        if len(office_working_day) == 0:
            office_working_day = OfficeWorkingDay.objects.create(
                office=office,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            office_working_day.save()

# Section working_day ---------------------------------------------------


@receiver(post_save, sender=Section)
def section_working_day_create(sender, instance, created, **kwargs):
    if created:
        section = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        section_working_day = SectionWorkingDay.objects.select_related("section").filter(
            section=section,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(section_working_day) == 0:
            section_working_day = SectionWorkingDay.objects.create(
                section=section,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            section_working_day.save()
        section_working_day = SectionWorkingDay.objects.select_related("section").filter(
            section=section,
            date__year=now.year,
            date__month=now.month
        )
        if len(section_working_day) == 0:
            section_working_day = SectionWorkingDay.objects.create(
                section=section,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            section_working_day.save()

# Team working_day ---------------------------------------------------


@receiver(post_save, sender=Team)
def team_working_day_create(sender, instance, created, **kwargs):
    if created:
        team = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        team_working_day = TeamWorkingDay.objects.select_related("team").filter(
            team=team,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(team_working_day) == 0:
            team_working_day = TeamWorkingDay.objects.create(
                team=team,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            team_working_day.save()

        team_working_day = TeamWorkingDay.objects.select_related("team").filter(
            team=team,
            date__year=now.year,
            date__month=now.month
        )
        if len(team_working_day) == 0:
            team_working_day = TeamWorkingDay.objects.create(
                team=team,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            team_working_day.save()

# Position working_day ---------------------------------------------------


@receiver(post_save, sender=Position)
def position_working_day_create(sender, instance, created, **kwargs):
    if created:
        position = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        position_working_day = PositionWorkingDay.objects.select_related("position").filter(
            position=position,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(position_working_day) == 0:
            position_working_day = PositionWorkingDay.objects.create(
                position=position,
                working_days_count=days_in_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            position_working_day.save()

        position_working_day = PositionWorkingDay.objects.select_related("position").filter(
            position=position,
            date__year=now.year,
            date__month=now.month
        )
        if len(position_working_day) == 0:
            position_working_day = PositionWorkingDay.objects.create(
                position=position,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            position_working_day.save()
