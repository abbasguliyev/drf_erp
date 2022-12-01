##############################
SaleRange (Satış sayı Aralığı)
##############################

- "title"
    - create zamanı göndərilmir, start_count və end_count-a görə avtomatik create olacaq
    - (Başlıq - String)
- "start_count"
    - required.
    - (Başlanğıc satış sayı - İnteger)
- "end_count"
    - nullable
    - Boş göndərilərsə bu zaman title avtomatik "start_count+" şəklində olacaq,
        əgər start_count 0-dırsa sadəcə olaraq "start_count" şəklində olacaq.
    - (Son satış sayı - İnteger)

=====

+-----------------+
|SaleRange create |
+-----------------+

SaleRange create
----------------

- endpoint: "http://localhost:8000/api/v1/salaries/sale-range/"

.. code:: json

  {
    "start_count": 2,
    "end_count": 5
  }


+-----------------+
|Update SaleRange |
+-----------------+

Update SaleRange
----------------

- endpoint: "http://localhost:8000/api/v1/salaries/sale-range/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "title": "2-5",
    "start_count": 2,
    "end_count": 5
  }

+------------------+
|Get All SaleRange |
+------------------+

Get All SaleRange
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/sale-range/"


+--------------------+
|Get SaleRange By ID |
+--------------------+

Get SaleRange By ID
-------------------

- endpoint: "http://localhost:8000/api/v1/salaries/sale-range/1/"

+-----------------+
|Delete SaleRange |
+-----------------+

Delete SaleRange
----------------

- endpoint: "http://localhost:8000/api/v1/salaries/sale-range/1/"