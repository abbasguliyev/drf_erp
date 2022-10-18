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
- address
    - required. 
    - (Adres - String)
- phone
    - required. 
    - (tel_no - String)
- email
    - required. 
    - (Email - String)
- web_site
    - required. 
    - (Web site - String)
- office_count
    - Get sorğusunda gəlir, şirkətə tabe ofislərin sayını bildirir
    - (Ofis sayı - İnteger)
- employee_count
    - Get sorğusunda gəlir, şirkətə tabe işçilərin sayını bildirir
    - (İşçi sayı - İnteger)

=====

+---------------+
|Company create |
+---------------+

Company create
--------------

- endpoint: "http://localhost:8000/api/v1/company/"

.. code:: json

  {
    "name": "Test",
    "address": "Baku Nerimanov",
    "phone": "65465656",
    "email": "ocean@example.com",
    "web_site": "ocean.az"
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
    "name": "Test",
    "address": "Baku Nerimanov",
    "phone": "65465656",
    "email": "ocean@example.com",
    "web_site": "ocean.az",
    "is_active": true
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