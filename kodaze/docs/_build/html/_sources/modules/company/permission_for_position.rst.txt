#############################################
Permission For Position (Vəzifəyə görə icazə)
#############################################

- position_id
    - required.
    - Mutleq gonderilmelidir
    - (Vəzifə İD - Position)
- permission_group_id
    - required.
    - Mutleq gonderilmelidir
    - (Group İD - Group)

=====

+-------------------------------+
|Permission For Position create |
+-------------------------------+

Permission For Position create
------------------------------

- endpoint: "http://localhost:8000/api/v1/company/position-permissions/"

.. code:: json

  {
    "position_id": null,
    "permission_group_id": null
  }

+-------------------------------+
|Update Permission For Position |
+-------------------------------+

Update Permission For Position
------------------------------

- endpoint: "http://localhost:8000/api/v1/company/position-permissions/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "position_id": null,
    "permission_group_id": null
  }

+--------------------------------+
|Get All Permission For Position |
+--------------------------------+

Get All Permission For Position
-------------------------------

- endpoint: "http://localhost:8000/api/v1/company/position-permissions/"


+----------------------------------+
|Get Permission For Position By ID |
+----------------------------------+

Get Permission For Position By ID
---------------------------------

- endpoint: "http://localhost:8000/api/v1/company/position-permissions/1/"

+-------------------------------+
|Delete Permission For Position |
+-------------------------------+

Delete Permission For Position
------------------------------

- endpoint: "http://localhost:8000/api/v1/company/position-permissions/1/"