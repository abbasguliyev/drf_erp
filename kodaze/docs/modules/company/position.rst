#################
Position (Vəzifə)
#################

- name
    - required. 
    - Mutleq gonderilmelidir
    - (Position adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)
- company_id
    - required. 
    - Mutleq gonderilmelidir
    - (Şirkət İD - Company)

=====

+----------------+
|Position create |
+----------------+

Position create
---------------

- endpoint: "http://localhost:8000/api/v1/company/positions/"

.. code:: json

  {
    "company_id": null,
    "name": "",
    "is_active": false
  }

+----------------+
|Update Position |
+----------------+

Update Position
---------------

- endpoint: "http://localhost:8000/api/v1/company/positions/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "company_id": null,
    "name": "",
    "is_active": false
  }

+-----------------+
|Get All Position |
+-----------------+

Get All Position
----------------

- endpoint: "http://localhost:8000/api/v1/company/positions/"


+-------------------+
|Get Position By ID |
+-------------------+

Get Position By ID
------------------

- endpoint: "http://localhost:8000/api/v1/company/positions/1/"

+--------------------+
|Deactivate Position |
+--------------------+

Deactivate Position
-------------------

- endpoint: "http://localhost:8000/api/v1/company/positions/1/"
- Vəzifəni deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.