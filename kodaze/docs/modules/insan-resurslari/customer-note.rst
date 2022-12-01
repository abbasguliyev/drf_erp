################################
Customer Note (Müştəri Qeydləri)
################################

- customer_id
    - required. 
    - Mutleq gonderilmelidir
    - (Müştəri İD - Customer)
- note
    - required. 
    - Mutleq gonderilmelidir
    - (Qeyd - String)
- date
    - göndərilmir. Arxada avtomatik create olur. 
    - (Create Date - Date)

=====

+---------------------+
|Customer Note create |
+---------------------+

Customer Note create
--------------------

- endpoint: "http://localhost:8000/api/v1/users/customer-notes/"

.. code:: json

  {
    "customer_id": null,
    "note": ""
  }

+---------------------+
|Update Customer Note |
+---------------------+

Update Customer Note
--------------------

- endpoint: "http://localhost:8000/api/v1/users/customer-notes/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "customer_id": null,
    "note": ""
  }

+----------------------+
|Get All Customer Note |
+----------------------+

Get All Customer Note
---------------------

- endpoint: "http://localhost:8000/api/v1/users/customer-notes/"


+------------------------+
|Get Customer Note By ID |
+------------------------+

Get Customer Note By ID
-----------------------

- endpoint: "http://localhost:8000/api/v1/users/customer-notes/1/"

+---------------------+
|Delete Customer Note |
+---------------------+

Delete Customer Note
--------------------

- endpoint: "http://localhost:8000/api/v1/users/customer-notes/1/"