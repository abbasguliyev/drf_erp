#########################
SalaryPunishment (Cərimə)
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

+------------------------+
|SalaryPunishment create |
+------------------------+

SalaryPunishment create
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/"

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+------------------------+
|Update SalaryPunishment |
+------------------------+

Update SalaryPunishment
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+-------------------------+
|Get All SalaryPunishment |
+-------------------------+

Get All SalaryPunishment
------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/"


+---------------------------+
|Get SalaryPunishment By ID |
+---------------------------+

Get SalaryPunishment By ID
--------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"

+------------------------+
|Delete SalaryPunishment |
+------------------------+

Delete SalaryPunishment
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"