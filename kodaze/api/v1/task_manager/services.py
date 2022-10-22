from datetime import date

from rest_framework.exceptions import ValidationError
from company.models import Position
from task_manager import ICRA_EDILIR
from task_manager.models import TaskManager

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
        user_list = user_str.split(',')
    else:
        user_list = None

    if position_list is not None:
        for p_id in position_list:
            pst = Position.objects.get(pk=p_id)
            users = User.objects.filter(position=pst)
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
    if user_list is not None:
        for user_id in user_list:
            user = User.objects.get(pk=user_id)
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
