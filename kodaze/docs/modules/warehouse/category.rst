#####################
Category (Kateqoriya)
#####################

- "category_name"
    - required. 
    - Mutleq gonderilmelidir
    - (Adı - String)

=====

+----------------+
|Category create |
+----------------+

Category create
---------------

- endpoint: "http://localhost:8000/api/v1/product/categories/"

.. code:: json

  {
    "category_name": ""
  }

+----------------+
|Update Category |
+----------------+

Update Category
---------------

- endpoint: "http://localhost:8000/api/v1/product/categories/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "category_name": ""
  }

+-----------------+
|Get All Category |
+-----------------+

Get All Category
----------------

- endpoint: "http://localhost:8000/api/v1/product/categories/"


+-------------------+
|Get Category By ID |
+-------------------+

Get Category By ID
------------------

- endpoint: "http://localhost:8000/api/v1/product/categories/1/"

+----------------+
|Delete Category |
+----------------+

Delete Category
---------------

- endpoint: "http://localhost:8000/api/v1/product/categories/1/"