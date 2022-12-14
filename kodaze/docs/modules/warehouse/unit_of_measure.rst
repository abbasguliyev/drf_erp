###########################
UnitOfMeasure (Ölçü vahidi)
###########################

- "name"
    - required. 
    - Mutleq gonderilmelidir
    - (Adı - String)

=====

+---------------------+
|UnitOfMeasure create |
+---------------------+

UnitOfMeasure create
--------------------

- endpoint: "http://localhost:8000/api/v1/product/unit-of-measure/"

.. code:: json

  {
    "name": ""
  }

+---------------------+
|Update UnitOfMeasure |
+---------------------+

Update UnitOfMeasure
--------------------

- endpoint: "http://localhost:8000/api/v1/product/unit-of-measure/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "name": ""
  }

+----------------------+
|Get All UnitOfMeasure |
+----------------------+

Get All UnitOfMeasure
---------------------

- endpoint: "http://localhost:8000/api/v1/product/unit-of-measure/"


+------------------------+
|Get UnitOfMeasure By ID |
+------------------------+

Get UnitOfMeasure By ID
-----------------------

- endpoint: "http://localhost:8000/api/v1/product/unit-of-measure/1/"

+---------------------+
|Delete UnitOfMeasure |
+---------------------+

Delete UnitOfMeasure
--------------------

- endpoint: "http://localhost:8000/api/v1/product/unit-of-measure/1/"