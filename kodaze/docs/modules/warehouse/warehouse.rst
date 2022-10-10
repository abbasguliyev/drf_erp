#################
Warehouse (Anbar)
#################

- "name"
    - required.
    - (Anbar adı - String)
- "office_id"
    - nullable.
    - (Ofis İD - Office)
- "company_id"
    - nullable
    - (Şirkət İD - Company)
- "is_active"
    - default: true.
    - create zamanı json içində göndərməyə ehtiyac yoxdur.
    - (Aktiv/Deaktiv - Boolean)

=====

+-----------------+
|Warehouse create |
+-----------------+

Warehouse create
----------------

- endpoint: "http://localhost:8000/api/v1/warehouse/"

.. code:: json

  {
    "company_id": null,
    "office_id": null,
    "name": ""
  }

+-----------------+
|Update Warehouse |
+-----------------+

Update Warehouse
----------------

- endpoint: "http://localhost:8000/api/v1/warehouse/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "company_id": null,
    "office_id": null,
    "name": "",
    "is_active": true
  }

+------------------+
|Get All Warehouse |
+------------------+

Get All Warehouse
-----------------

- endpoint: "http://localhost:8000/api/v1/warehouse/"


+--------------------+
|Get Warehouse By ID |
+--------------------+

Get Warehouse By ID
-------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/1/"

+----------------------+
|Deactivated Warehouse |
+----------------------+

Deactivated Warehouse
---------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/1/"
- Anbarı deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.