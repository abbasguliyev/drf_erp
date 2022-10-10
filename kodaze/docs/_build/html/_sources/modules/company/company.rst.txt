################
Company (Şirkət)
################

- name
    - required. 
    - unique
    - Mutleq gonderilmelidir
    - (Company adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)
- holding
    - required. 
    - Mutleq gonderilmelidir
    - (Holdinq İD - Holding)

=====

+---------------+
|Company create |
+---------------+

Company create
--------------

- endpoint: "http://localhost:8000/api/v1/company/"

.. code:: json

  {
    "is_active": false,
    "name": "",
    "holding": null
  }

+---------------+
|Update Company |
+---------------+

Update Company
--------------

- endpoint: "http://localhost:8000/api/v1/company/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "is_active": false,
    "name": "",
    "holding": null
  }

+----------------+
|Get All Company |
+----------------+

Get All Company
---------------

- endpoint: "http://localhost:8000/api/v1/company/"


+------------------+
|Get Company By ID |
+------------------+

Get Company By ID
-----------------

- endpoint: "http://localhost:8000/api/v1/company/1/"

+-------------------+
|Deactivate Company |
+-------------------+

Deactivate Company
------------------

- endpoint: "http://localhost:8000/api/v1/company/1/"
- Şirkət-i deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.