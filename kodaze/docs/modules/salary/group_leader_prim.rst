######################################
GroupLeaderPrim (Qrup Lider Komissiya)
######################################

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

+-----------------------+
|GroupLeaderPrim create |
+-----------------------+

GroupLeaderPrim create
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/group-leader-prim/"

.. code:: json

  {
    "prim_status_id": 5,
    "position_id": 2,
    "cash": 180,
    "installment_4_12": 160,
    "installment_13_18": 140,
    "installment_19_24": 120
  }

+-----------------------+
|Update GroupLeaderPrim |
+-----------------------+

Update GroupLeaderPrim
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/group-leader-prim/1/"
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

+------------------------+
|Get All GroupLeaderPrim |
+------------------------+

Get All GroupLeaderPrim
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/group-leader-prim/"


+--------------------------+
|Get GroupLeaderPrim By ID |
+--------------------------+

Get GroupLeaderPrim By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/group-leader-prim/1/"

+-----------------------+
|Delete GroupLeaderPrim |
+-----------------------+

Delete GroupLeaderPrim
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/group-leader-prim/1/"