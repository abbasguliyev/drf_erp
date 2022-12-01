##############################
Employee Status (İşçi Statusu)
##############################

- status_name
    - required. 
    - Mutleq gonderilmelidir
    - (Status adı - String)

=====

+-----------------------+
|Employee Status create |
+-----------------------+

Employee Status create
----------------------

- endpoint: "http://localhost:8000/api/v1/users/employee-status/"

.. code:: json

  {
    "status_name": ""
  }

+-----------------------+
|Update Employee Status |
+-----------------------+

Update Employee Status
----------------------

- endpoint: "http://localhost:8000/api/v1/users/employee-status/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "status_name": ""
  }

+------------------------+
|Get All Employee Status |
+------------------------+

Get All Employee Status
-----------------------

- endpoint: "http://localhost:8000/api/v1/users/employee-status/"


+--------------------------+
|Get Employee Status By ID |
+--------------------------+

Get Employee Status By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/users/employee-status/1/"

+-----------------------+
|Delete Employee Status |
+-----------------------+

Delete Employee Status
----------------------

- endpoint: "http://localhost:8000/api/v1/users/employee-status/1/"