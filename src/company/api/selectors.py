from django.db.models.query import QuerySet
from company.models import (
    Holding,
    Company,
    Department,
    Office,
    Section,
    Position,
    Team,
    AppLogo
)


def holding_list(*, filters=None) -> QuerySet[Holding]:
    filters = filters or {}
    qs = Holding.objects.all()
    return qs

def company_list(*, filters=None) -> QuerySet[Company]:
    filters = filters or {}
    qs = Company.objects.all()
    return qs

def department_list(*, filters=None) -> QuerySet[Department]:
    filters = filters or {}
    qs = Department.objects.all()
    return qs

def office_list(*, filters=None) -> QuerySet[Office]:
    filters = filters or {}
    qs = Office.objects.select_related('company').all()
    return qs

def section_list(*, filters=None) -> QuerySet[Section]:
    filters = filters or {}
    qs = Section.objects.all()
    return qs

def position_list(*, filters=None) -> QuerySet[Position]:
    filters = filters or {}
    qs = Position.objects.all()
    return qs

def team_list(*, filters=None) -> QuerySet[Team]:
    filters = filters or {}
    qs = Team.objects.all()
    return qs

def applogo_list(*, filters=None) -> QuerySet[AppLogo]:
    filters = filters or {}
    qs = AppLogo.objects.all()
    return qs
