#########################
SalaryDeduction (Kəsinti)
#########################

- "employee_id"
    - required
    - (işçi id - User)
- "note"
    - nullable.
    - (qeyd - String)
- "date"
    - required
    - (tarix - Date)
- "amount"
    - required
    - (məbləğ - Float)

=====

+-----------------------+
|SalaryDeduction create |
+-----------------------+

SalaryDeduction create
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/"

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+-----------------------+
|Update SalaryDeduction |
+-----------------------+

Update SalaryDeduction
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+------------------------+
|Get All SalaryDeduction |
+------------------------+

Get All SalaryDeduction
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/"


+--------------------------+
|Get SalaryDeduction By ID |
+--------------------------+

Get SalaryDeduction By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"

+-----------------------+
|Delete SalaryDeduction |
+-----------------------+

Delete SalaryDeduction
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"