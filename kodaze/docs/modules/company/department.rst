########################
Department (Departament)
########################

- name
    - required. 
    - Mutleq gonderilmelidir
    - (Department adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)
- holding_id
    - required. 
    - Mutleq gonderilmelidir
    - (Holdinq İD - Holding)

=====

+------------------+
|Department create |
+------------------+

Department create
-----------------

- endpoint: "http://localhost:8000/api/v1/company/departments/"

.. code:: json

  {
    "holding_id": null,
    "name": "",
    "is_active": false
  }

+------------------+
|Update Department |
+------------------+

Update Department
-----------------

- endpoint: "http://localhost:8000/api/v1/company/departments/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "holding_id": null,
    "name": "",
    "is_active": false
  }

+-------------------+
|Get All Department |
+-------------------+

Get All Department
------------------

- endpoint: "http://localhost:8000/api/v1/company/departments/"


+---------------------+
|Get Department By ID |
+---------------------+

Get Department By ID
--------------------

- endpoint: "http://localhost:8000/api/v1/company/departments/1/"

+----------------------+
|Deactivate Department |
+----------------------+

Deactivate Department
---------------------

- endpoint: "http://localhost:8000/api/v1/company/departments/1/"
- Departamenti deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.