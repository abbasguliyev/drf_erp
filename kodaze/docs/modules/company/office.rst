#############
Office (Ofis)
#############

- name
    - required. 
    - Mutleq gonderilmelidir
    - (Office adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)
- company_id
    - required. 
    - Mutleq gonderilmelidir
    - (Şirkət İD - Company)

=====

+--------------+
|Office create |
+--------------+

Office create
-------------

- endpoint: "http://localhost:8000/api/v1/company/offices/"

.. code:: json

  {
    "company_id": null,
    "name": "",
    "is_active": false
  }

+--------------+
|Update Office |
+--------------+

Update Office
-------------

- endpoint: "http://localhost:8000/api/v1/company/offices/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "company_id": null,
    "name": "",
    "is_active": false
  }

+---------------+
|Get All Office |
+---------------+

Get All Office
--------------

- endpoint: "http://localhost:8000/api/v1/company/offices/"


+-----------------+
|Get Office By ID |
+-----------------+

Get Office By ID
----------------

- endpoint: "http://localhost:8000/api/v1/company/offices/1/"

+------------------+
|Deactivate Office |
+------------------+

Deactivate Office
-----------------

- endpoint: "http://localhost:8000/api/v1/company/offices/1/"
- Ofisi deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.