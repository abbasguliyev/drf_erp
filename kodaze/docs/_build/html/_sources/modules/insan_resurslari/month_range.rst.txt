#######################
MonthRange (Ay Aralığı)
#######################

- "title"
    - create zamanı göndərilmir, start_month və end_month-a görə avtomatik create olacaq
    - (Başlıq - String)
- "start_month"
    - required.
    - (Başlanğıc ay - İnteger)
- "end_month"
    - nullable
    - Boş göndərilərsə bu zaman title avtomatik "start_month+" şəklində olacaq,
        əgər start_month 0-dırsa sadəcə olaraq "start_month" şəklində olacaq.
    - (Son ay - İnteger)

=====

+------------------+
|MonthRange create |
+------------------+

MonthRange create
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/month-range/"

.. code:: json

  {
    "start_month": 2,
    "end_month": 5
  }


+------------------+
|Update MonthRange |
+------------------+

Update MonthRange
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/month-range/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "title": "2-5",
    "start_month": 2,
    "end_month": 5
  }

+-------------------+
|Get All MonthRange |
+-------------------+

Get All MonthRange
------------------

- endpoint: "http://localhost:8000/api/v1/salaries/month-range/"


+---------------------+
|Get MonthRange By ID |
+---------------------+

Get MonthRange By ID
--------------------

- endpoint: "http://localhost:8000/api/v1/salaries/month-range/1/"

+------------------+
|Delete MonthRange |
+------------------+

Delete MonthRange
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/month-range/1/"