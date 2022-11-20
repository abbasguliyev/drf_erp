#############
Bonus (Bonus)
#############

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

+-------------+
|Bonus create |
+-------------+

Bonus create
------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/"

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+-------------+
|Update Bonus |
+-------------+

Update Bonus
------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "employee_id": 19,
    "amount": 50,
    "note": "test",
    "date": "01-11-2022"
  }

+--------------+
|Get All Bonus |
+--------------+

Get All Bonus
-------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/"


+----------------+
|Get Bonus By ID |
+----------------+

Get Bonus By ID
---------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"

+-------------+
|Delete Bonus |
+-------------+

Delete Bonus
------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"