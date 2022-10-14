###################################
Manager2Prim (Menecer 2 Komissiya)
###################################

- "prim_status_id"
    - required
    - (prim_status_id - User)
- "position_id"
    - required.
    - (position_id - String)
- "sale0"
    - nullable
    - (sale0 - Float)
- "sale1_8"
    - nullable
    - (sale1_8 - Float)
- "sale9_14"
    - nullable
    - (sale9_14 - Float)
- "sale15p"
    - nullable
    - (sale15p - Float)
- "sale20p"
    - nullable
    - (sale20p - Float)
- "prim_for_team"
    - nullable
    - (prim_for_team - Float)
- "prim_for_office"
    - nullable
    - (prim_for_office - Float)
- "fix_prim"
    - nullable
    - (fix_prim - Float)

=====

+--------------------+
|Manager2Prim create |
+--------------------+

Manager2Prim create
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager2-prim/"

.. code:: json

  {
    "prim_status_id": 1,
    "position_id": 5,
    "sale0": 500,
    "sale1_8": 250,
    "sale9_14": 60,
    "sale15p": 80,
    "sale20p": 100,
    "prim_for_team": 0,
    "prim_for_office": 0,
    "fix_prim": 0
  }

+--------------------+
|Update Manager2Prim |
+--------------------+

Update Manager2Prim
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager2-prim/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "prim_status_id": 1,
    "position_id": 5,
    "sale0": 500,
    "sale1_8": 250,
    "sale9_14": 60,
    "sale15p": 80,
    "sale20p": 100,
    "prim_for_team": 0,
    "prim_for_office": 0,
    "fix_prim": 0
  }

+---------------------+
|Get All Manager2Prim |
+---------------------+

Get All Manager2Prim
--------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager2-prim/"


+-----------------------+
|Get Manager2Prim By ID |
+-----------------------+

Get Manager2Prim By ID
----------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager2-prim/1/"

+--------------------+
|Delete Manager2Prim |
+--------------------+

Delete Manager2Prim
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/manager2-prim/1/"