###########################
Office CashBox (Ofis Kassa)
###########################

- company_id
    - required. 
    - Mutleq gonderilmelidir
    - (Ofis ID - Office)
- balance
    - required. 
    - Mutleq gonderilmelidir
    - (balans - Float)

=====

+----------------------+
|Office CashBox create |
+----------------------+

Office CashBox create
---------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/office-cashbox/"

.. code:: json

  {
    "office_id": null,
    "balance": null
  }

+----------------------+
|Update Office CashBox |
+----------------------+

Update Office CashBox
---------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/office-cashbox/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "office_id": null,
    "balance": null
  }

+-----------------------+
|Get All Office CashBox |
+-----------------------+

Get All Office CashBox
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/office-cashbox/"


+-------------------------+
|Get Office CashBox By ID |
+-------------------------+

Get Office CashBox By ID
------------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/office-cashbox/1/"

+----------------------+
|Delete Office CashBox |
+----------------------+

Delete Office CashBox
---------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/office-cashbox/1/"