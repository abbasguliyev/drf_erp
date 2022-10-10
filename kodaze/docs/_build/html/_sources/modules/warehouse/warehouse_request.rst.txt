###############################
Warehouse Request (Anbar Sorğu)
###############################

- "warehouse_id"
    - required.
    - Sorğu göndərilən anbar - Anbar id
    - (Anbar ID - Warehouse)
- "employee_who_sent_the_request_id"
    - göndərilmir default login olan user olur
    - (Sorğu göndərən işçinin İD-si - User)
- "product_and_quantity"
    - nullable
    - məhsulun id-si və neçə dənə lazım olduğu "1-100" formatında yazılır, əgər bir neçə məhsul və say göndəriləcəksə "1-100,2-50,3-60" formasında göndərilməlidir
    - (Məhsul və sayı - String)
- "note"
    - nullable
    - (Qeyd - String)
- "is_done"
    - default: true.
    - create zamanı json içində göndərilmir.
    - (Yerniə yetirildi - Boolean)
- "request_date"
    - Json içində göndərilmir. Avtomatik göndərilmə tarixi götürülür.
    - (Sorğu tarixi - Date)

=====

+-------------------------+
|Warehouse Request create |
+-------------------------+

Warehouse Request create
------------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/"

.. code:: json

  {
    "warehouse_id": null,
    "employee_who_sent_the_request_id": null,
    "product_and_quantity": "",
    "note": ""
  }

+-------------------------+
|Update Warehouse Request |
+-------------------------+

Update Warehouse Request
------------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "warehouse_id": null,
    "employee_who_sent_the_request_id": null,
    "product_and_quantity": "",
    "note": "",
    "is_done": false
  }

+--------------------------+
|Get All Warehouse Request |
+--------------------------+

Get All Warehouse Request
-------------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/"


+----------------------------+
|Get Warehouse Request By ID |
+----------------------------+

Get Warehouse Request By ID
---------------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/1/"

+-------------------------+
|Delete Warehouse Request |
+-------------------------+

Delete Warehouse Request
------------------------

- endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/1/"