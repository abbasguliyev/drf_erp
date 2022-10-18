#################
Holding (Holdinq)
#################

- name
    - required. 
    - unique
    - (Holding adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)

=====

+---------------+
|Holding create |
+---------------+

Holding create
--------------

- endpoint: "http://localhost:8000/api/v1/company/holding/"

.. code:: json

  {
    "name": ""
  }

+---------------+
|Update Holding |
+---------------+

Update Holding
--------------

- endpoint: "http://localhost:8000/api/v1/company/holding/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "is_active": false,
    "name": ""
  }

+----------------+
|Get All Holding |
+----------------+

Get All Holding
---------------

- endpoint: "http://localhost:8000/api/v1/company/holding/"


+------------------+
|Get Holding By ID |
+------------------+

Get Holding By ID
-----------------

- endpoint: "http://localhost:8000/api/v1/company/holding/1/"

+-------------------+
|Deactivate Holding |
+-------------------+

Deactivate Holding
------------------

- endpoint: "http://localhost:8000/api/v1/company/holding/1/"
- Holdinq-i deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.