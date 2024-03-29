from datetime import date

from rest_framework.exceptions import ValidationError
from company.models import Position
from task_manager.models import TaskManager
from account.api.selectors import user_list
from django.contrib.auth import get_user_model

User = get_user_model()


def task_manager_create(
        *, creator,
        title: str,
        body: str,
        created_date: date = date.today(),
        end_date: date,
        users: str = None,
        positions: str = None,
        employee=None,
        position=None,
) -> TaskManager:
    if users == None and positions == None:
        raise ValidationError({'detail': "İşçi və ya vəzifədən biri mütləq seçilməlidir"})

    position_str = positions
    if position_str is not None:
        position_list = position_str.split(',')
    else:
        position_list = None
    user_str = users
    if user_str is not None:
        emp_list = user_str.split(',')
    else:
        emp_list = None

    if position_list is not None:
        for p_id in position_list:
            pst = position_list().filter(pk=p_id).last()
            users = user_list().filter(position= pst)
            for user in users:
                task_manager = TaskManager.objects.create(
                    creator=creator,
                    title=title,
                    body=body,
                    created_date=created_date,
                    end_date=end_date,
                    position=pst,
                    employee=user,
                )
                task_manager.save()
    if emp_list is not None:
        for user_id in emp_list:
            user = user_list().filter(pk= user_id).last()
            task_manager = TaskManager.objects.create(
                creator=creator,
                title=title,
                body=body,
                created_date=created_date,
                end_date=end_date,
                employee=user,
            )
            task_manager.save()

    return task_manager
