###################################
Manager1Prim (Menecer 1 Komissiya)
###################################

- "prim_status_id"
    - required
    - (prim_status_id - User)
- "position_id"
    - required.
    - (position_id - String)
- "cash"
    - nullable
    - (cash - Float)
- "installment_4_12"
    - nullable
    - (installment_4_12 - Float)
- "installment_13_18"
    - nullable
    - (installment_13_18 - Float)
- "installment_19_24"
    - nullable
    - (installment_19_24 - Float)

=====

+--------------------+
|Manager1Prim create |
+--------------------+

Manager1Prim create
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager1-prim/"

.. code:: json

  {
    "prim_status_id": 5,
    "position_id": 2,
    "cash": 180,
    "installment_4_12": 160,
    "installment_13_18": 140,
    "installment_19_24": 120
  }

+--------------------+
|Update Manager1Prim |
+--------------------+

Update Manager1Prim
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager1-prim/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "prim_status_id": 5,
    "position_id": 2,
    "cash": 180,
    "installment_4_12": 160,
    "installment_13_18": 140,
    "installment_19_24": 120
  }

+---------------------+
|Get All Manager1Prim |
+---------------------+

Get All Manager1Prim
--------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager1-prim/"


+-----------------------+
|Get Manager1Prim By ID |
+-----------------------+

Get Manager1Prim By ID
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager1-prim/1/"

+--------------------+
|Delete Manager1Prim |
+--------------------+

Delete Manager1Prim
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager1-prim/1/"