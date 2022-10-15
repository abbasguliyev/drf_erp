####################
PaySalary (Maaş ödə)
####################

- "employee"
    - required
    - (işçi id - User)
- "note"
    - nullable.
    - (qeyd - String)
- "date"
    - required
    - (tarix - Date)

=====

+-----------------+
|PaySalary create |
+-----------------+

PaySalary create
----------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/"

.. code:: json

  {
    "employee": 1,
    "note": "test",
    "salary_date": "15-10-2022"
  }

+------------------+
|Get All PaySalary |
+------------------+

Get All PaySalary
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/"


+--------------------+
|Get PaySalary By ID |
+--------------------+

Get PaySalary By ID
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"