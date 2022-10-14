########################################
OfficeLeaderPrim (Ofis Lider Komissiya)
########################################

- "prim_status"
    - required
    - (İşçi - User)
- "position_id"
    - required.
    - (qeyd - String)
- "prim_for_office"
    - nullable
    - (prim_for_office - Float)
- "fix_prim"
    - nullable
    - (fix_prim - Float)

=====

+------------------------+
|OfficeLeaderPrim create |
+------------------------+

OfficeLeaderPrim create
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/office-leader-prim/"

.. code:: json

  {
    "prim_status_id": 5,
    "position_id": 2,
    "prim_for_office": 100,
    "fix_prim": 0
  }

+------------------------+
|Update OfficeLeaderPrim |
+------------------------+

Update OfficeLeaderPrim
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/office-leader-prim/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "prim_status_id": 5,
    "position_id": 2,
    "prim_for_office": 100,
    "fix_prim": 0
  }

+-------------------------+
|Get All OfficeLeaderPrim |
+-------------------------+

Get All OfficeLeaderPrim
------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/office-leader-prim/"


+---------------------------+
|Get OfficeLeaderPrim By ID |
+---------------------------+

Get OfficeLeaderPrim By ID
--------------------------

- endpoint: "http://localhost:8000/api/v1/salaries/office-leader-prim/1/"

+------------------------+
|Delete OfficeLeaderPrim |
+------------------------+

Delete OfficeLeaderPrim
-----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/office-leader-prim/1/"