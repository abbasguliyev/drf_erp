##############
Logo (Logo)
##############

- logo
    - required.
    - Mutleq gonderilmelidir
    - (Logo - İmage)

=====

+------------+
|Logo create |
+------------+

Logo create
-----------

- endpoint: "http://localhost:8000/api/v1/company/logo/"

.. code:: json

  {
    "logo": null
  }

+------------+
|Update Logo |
+------------+

Update Logo
-----------

- endpoint: "http://localhost:8000/api/v1/company/logo/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "logo": null
  }

+-------------+
|Get All Logo |
+-------------+

Get All Logo
------------

- endpoint: "http://localhost:8000/api/v1/company/logo/"


+---------------+
|Get Logo By ID |
+---------------+

Get Logo By ID
--------------

- endpoint: "http://localhost:8000/api/v1/company/logo/1/"

+------------+
|Delete Logo |
+------------+

Delete Logo
-----------

- endpoint: "http://localhost:8000/api/v1/company/logo/1/"