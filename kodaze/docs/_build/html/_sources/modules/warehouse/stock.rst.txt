############
Stock (Stok)
############

- "warehouse_id"
    - required.
    - (Anbar İD - Warehouse)
- "product_id"
    - required
    - (Məhsul İD - Product)
- "note"
    - nullable.
    - (Qeyd - String)
- "quantity"
    - required
    - (Say - Integer)
- "date"
    - göndərilmir, avtomatik create olunma tarixini götürür
    - (Tarix - Date)

=====

+-------------+
|Stock create |
+-------------+

Stock create
------------

- endpoint: "http://localhost:8000/api/v1/warehouse/stocks/"

.. code:: json

  {
    "warehouse_id": null,
    "product_id": null,
    "quantity": null,
    "note": ""
  }

+-------------+
|Update Stock |
+-------------+

Update Stock
------------

- endpoint: "http://localhost:8000/api/v1/warehouse/stocks/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "warehouse_id": null,
    "product_id": null,
    "quantity": null,
    "note": ""
  }

+--------------+
|Get All Stock |
+--------------+

Get All Stock
-------------

- endpoint: "http://localhost:8000/api/v1/warehouse/stocks/"


+----------------+
|Get Stock By ID |
+----------------+

Get Stock By ID
---------------

- endpoint: "http://localhost:8000/api/v1/warehouse/stocks/1/"

+-------------+
|Delete Stock |
+-------------+

Delete Stock
------------

- endpoint: "http://localhost:8000/api/v1/warehouse/stocks/1/"