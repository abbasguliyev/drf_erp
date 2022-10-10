##############
Team (Komanda)
##############

- name
    - required. 
    - unique
    - Mutleq gonderilmelidir
    - (Team adı - String)
- is_active
    - create zamanı göndərilmir. Update zamanı istəyə görə göndərilir. 
    - (Aktiv/Deaktiv - Boolean)

=====

+------------+
|Team create |
+------------+

Team create
-----------

- endpoint: "http://localhost:8000/api/v1/company/teams/"

.. code:: json

  {
    "is_active": false,
    "name": ""
  }

+------------+
|Update Team |
+------------+

Update Team
-----------

- endpoint: "http://localhost:8000/api/v1/company/teams/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "is_active": false,
    "name": ""
  }

+-------------+
|Get All Team |
+-------------+

Get All Team
------------

- endpoint: "http://localhost:8000/api/v1/company/teams/"


+---------------+
|Get Team By ID |
+---------------+

Get Team By ID
--------------

- endpoint: "http://localhost:8000/api/v1/company/teams/1/"

+----------------+
|Deactivate Team |
+----------------+

Deactivate Team
---------------

- endpoint: "http://localhost:8000/api/v1/company/teams/1/"
- Komandannı deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.