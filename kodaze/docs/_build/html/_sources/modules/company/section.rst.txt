##############
Section (Şöbə)
##############

- name
    - required. 
    - Mutleq gonderilmelidir
    - (Section adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)
- office_id
    - required. 
    - Mutleq gonderilmelidir
    - (Ofis İD - Office)

=====

+---------------+
|Section create |
+---------------+

Section create
--------------

- endpoint: "http://localhost:8000/api/v1/company/sections/"

.. code:: json

  {
    "office_id": null,
    "name": "",
    "is_active": false
  }

+---------------+
|Update Section |
+---------------+

Update Section
--------------

- endpoint: "http://localhost:8000/api/v1/company/sections/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "office_id": null,
    "name": "",
    "is_active": false
  }

+----------------+
|Get All Section |
+----------------+

Get All Section
---------------

- endpoint: "http://localhost:8000/api/v1/company/sections/"


+------------------+
|Get Section By ID |
+------------------+

Get Section By ID
-----------------

- endpoint: "http://localhost:8000/api/v1/company/sections/1/"

+-------------------+
|Deactivate Section |
+-------------------+

Deactivate Section
------------------

- endpoint: "http://localhost:8000/api/v1/company/sections/1/"
- Şöbəni deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.