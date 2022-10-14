#######################
AdvancedPayment (Avans)
#######################

- "employee_id"
    - required
    - (işmi id - User)
- "note"
    - nullable.
    - (qeyd - String)
- "date"
    - required
    - (tarix - Date)

=====

+-----------------------+
|AdvancedPayment create |
+-----------------------+

AdvancedPayment create
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/"
- Avans hər işçiyə eyni ay ərzində 2 dəfə verilir, və işçinin maaşından hər səfərində 15% çıxılaraq verilir

.. code:: json

  {
    "employee_id": 18,
    "note": "test",
    "date": "01-11-2022"
  }

+-----------------------+
|Update AdvancedPayment |
+-----------------------+

Update AdvancedPayment
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "employee_id": 18,
    "note": "test",
    "date": "01-11-2022"
  }

+------------------------+
|Get All AdvancedPayment |
+------------------------+

Get All AdvancedPayment
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/"


+--------------------------+
|Get AdvancedPayment By ID |
+--------------------------+

Get AdvancedPayment By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"

+-----------------------+
|Delete AdvancedPayment |
+-----------------------+

Delete AdvancedPayment
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"