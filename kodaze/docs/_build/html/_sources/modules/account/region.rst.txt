##############
Region (Bölgə)
##############

- region_name
    - required. 
    - Mutleq gonderilmelidir
    - (Bölgə adı - String)

=====

+------------------+
|All Region create |
+------------------+

All Region create
-----------------

- endpoint: "http://localhost:8000/api/v1/users/all-region-create/"
- Boş json ilə post sorğusu göndərilir. Avtomatik backend-də olan cities.json-da qeyd olunmuş bölgələr database-d əlavə olunur

.. code:: json

  {}

+--------------+
|Region create |
+--------------+

Region create
-------------

- endpoint: "http://localhost:8000/api/v1/users/region/"

.. code:: json

  {
    "region_name": ""
  }


+--------------+
|Update Region |
+--------------+

Update Region
-------------

- endpoint: "http://localhost:8000/api/v1/users/region/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "region_name": ""
  }

+---------------+
|Get All Region |
+---------------+

Get All Region
--------------

- endpoint: "http://localhost:8000/api/v1/users/region/"


+-----------------+
|Get Region By ID |
+-----------------+

Get Region By ID
----------------

- endpoint: "http://localhost:8000/api/v1/users/region/1/"

+--------------+
|Delete Region |
+--------------+

Delete Region
-------------

- endpoint: "http://localhost:8000/api/v1/users/region/1/"