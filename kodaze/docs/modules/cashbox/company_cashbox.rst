##############################
Company CashBox (Şirkət Kassa)
##############################

- company_id
    - required. 
    - Mutleq gonderilmelidir
    - (Şirkət ID - Company)
- balance
    - required. 
    - Mutleq gonderilmelidir
    - (balans - Float)

=====

+-----------------------+
|Company CashBox create |
+-----------------------+

Company CashBox create
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox/"

.. code:: json

  {
    "company_id": null,
    "balance": null
  }

+-----------------------+
|Update Company CashBox |
+-----------------------+

Update Company CashBox
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "company_id": null,
    "balance": null
  }

+------------------------+
|Get All Company CashBox |
+------------------------+

Get All Company CashBox
-----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox/"


+--------------------------+
|Get Company CashBox By ID |
+--------------------------+

Get Company CashBox By ID
-------------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox/1/"

+-----------------------+
|Delete Company CashBox |
+-----------------------+

Delete Company CashBox
----------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox/1/"