from salary.models import SalaryView
import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

def change_final_salary_when_update_user_const_salary(func):
    """
    İşçinin sabit əməkhaqqısı dəyişildiyi zaman həmin ayın maaş cədvəlindədə düzəliş edən dekorator
    """
    def wrapper(*args, **kwargs):
        id = args[0]
        
        try:
            salary = kwargs["salary"]
        except:
            salary = None

        if salary is not None:
            user = User.objects.get(pk=id)

            difference = 0
            old_salary = user.salary

            now = datetime.date.today()
            this_month = f"{now.year}-{now.month}-{1}"
            salary_view = SalaryView.objects.get(employee=user, date=this_month)

            if salary > old_salary:
                difference = salary - old_salary
                salary_view.final_salary = salary_view.final_salary + difference
                salary_view.save()
            elif salary < old_salary:
                difference = old_salary - salary
                salary_view.final_salary = salary_view.final_salary - difference
                salary_view.save()
        func(*args, **kwargs)
    return wrapper

