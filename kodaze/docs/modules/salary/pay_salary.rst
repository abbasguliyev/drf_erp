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
    - hansı tarixin maaşı ödənilməsi istənilirsə həmin tarix. 
        Yəni əgər bu ay ödənəcəksə prosesin edildiyi tarix göndərilə bilər, 
        backend üçün lazım olan ordakı il və aydır. Günün neçə daxil edilməsi önəmli deyil.
    - (tarix - Date)
- "salary_date"
    - nullable
    - Göndərilməsə bu
    - (maaşın ödənilmə tarixi - Date)

=====

+-----------------+
|PaySalary create |
+-----------------+

PaySalary create
----------------

- endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/"

.. code:: json

  {
    "employee": 21,
    "note": "maas odemek",
    "date": "01-10-2022",
    "salary_date": "15-10-2022"
  }

+------------------+
|Get All PaySalary |
+------------------+

Get All PaySalary
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/"


+--------------------+
|Get PaySalary By ID |
+--------------------+

Get PaySalary By ID
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/1/"