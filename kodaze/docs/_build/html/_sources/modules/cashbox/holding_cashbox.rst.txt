###############################
Holding CashBox (Holdinq Kassa)
###############################

- holding_id
    - required. 
    - Mutleq gonderilmelidir
    - (Holdinq ID - Holding)
- balance
    - required. 
    - Mutleq gonderilmelidir
    - (balans - Float)

=====

+-----------------------+
|Holding CashBox create |
+-----------------------+

Holding CashBox create
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox/"

.. code:: json

  {
    "holding_id": null,
    "balance": null
  }

+-----------------------+
|Update Holding CashBox |
+-----------------------+

Update Holding CashBox
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "holding_id": null,
    "balance": null
  }

+------------------------+
|Get All Holding CashBox |
+------------------------+

Get All Holding CashBox
-----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox/"


+--------------------------+
|Get Holding CashBox By ID |
+--------------------------+

Get Holding CashBox By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox/1/"

+-----------------------+
|Delete Holding CashBox |
+-----------------------+

Delete Holding CashBox
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox/1/"