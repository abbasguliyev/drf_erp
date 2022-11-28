#########
Əməkhaqqı
#########

+-----------------+
|Əməkhaqqı cədvəli|
+-----------------+

Əməkhaqqı cədvəli
-----------------

.. image:: _static/ss1.png
   :width: 1000px
   :height: 200px
   :alt: melumat
   :align: center

.. image:: _static/emekhaqqi.png
   :width: 1500px
   :height: 300px
   :alt: emekhaqqi cedveli
   :align: center

.. image:: _static/ss4.png
   :width: 300px
   :height: 300px
   :alt: json
   :align: center

- Json içində gələn datalar:
    - "employee" -> işçi - User (Şəkildəki ad soyad, şirkət, ofis, vəzifə, sabit məlumatları employee içində gəlir)
    - "total_working_day" -> iş günü - int
    - "sale_quantity" -> satış sayı - int
    - "commission_amount" -> komissiya - Float
    - "total_bonus" -> bonus - Float
    - "total_advancepayment" -> avans - Float
    - "total_salarydeduction" -> kəsinti - Float
    - "total_salarypunishment" -> cərimə - Float
    - "final_salary" -> yekun - Float
    - "pay_date" -> əmək haqqı ödəmə tarixi - Date
    - "is_done" -> status - Boolean
    - "date" -> tarix - Date

=====

- Bütün maaş cədvəlinə bax
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-views/"

- Filter: 
    - "http://localhost:8000/api/v1/salaries/salary-views/?employee=&employee__fullname=&employee__fullname__icontains=&employee__is_superuser=unknown&employee__salary_style=&employee__office=&employee__office__id=&employee__office__name=&employee__office__name__icontains=&employee__company=&employee__company__id=&employee__company__name=&employee__company__name__icontains=&employee__position=&employee__position__id=&employee__position__name=&employee__position__name__icontains=&employee__employee_status=&employee__employee_status__status_name=&employee__employee_status__status_name__icontains=&is_done=unknown&sale_quantity=&sale_quantity__gte=&sale_quantity__lte=&sales_amount=&sales_amount__gte=&sales_amount__lte=&final_salary=&final_salary__gte=&final_salary__lte=&date=&date__gte=&date__lte=&year=&month="

- Maaş cədvəlində id-ə görə axtarış
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-views/1/"


- Maaş cədvəlini excel-ə export etmək
    - endpoint: "http://localhost:8000/api/v1/salaries/export-data/"
    - export etmək üçün json içində list içində salary view(ə/h görüntüləmə) datasını göndərmək lazımdır.
    - Nümunə:

.. code:: json

  {
    "data": [
                {
                    "id": 1,
                    "employee": {
                        "id": 1,
                        "company": null,
                        "office": null,
                        "position": null,
                        "fullname": "",
                        "salary": 0.0
                    },
                    "sale_quantity": 0,
                    "commission_amount": 0.0,
                    "final_salary": 0.0,
                    "pay_date": "17-11-2022",
                    "is_done": true,
                    "extra_data": {
                        "total_advancepayment": 0,
                        "total_bonus": 0,
                        "total_salarydeduction": 0,
                        "total_salarypunishment": 0,
                        "total_working_day": 31
                    },
                    "date": "01-10-2022"
                },
                {
                    "id": 2,
                    "employee": {
                        "id": 1,
                        "company": null,
                        "office": null,
                        "position": null,
                        "fullname": "",
                        "salary": 0.0
                    },
                    "sale_quantity": 0,
                    "commission_amount": 0.0,
                    "final_salary": 0.0,
                    "pay_date": null,
                    "is_done": false,
                    "extra_data": {
                        "total_advancepayment": 0,
                        "total_bonus": 0,
                        "total_salarydeduction": 0,
                        "total_salarypunishment": 0,
                        "total_working_day": 30
                    },
                    "date": "01-11-2022"
                }
        ]
  }

+-----+
|Avans|
+-----+

Avans
-----

.. image:: _static/ss2.png
   :width: 1000px
   :height: 40px
   :align: center

.. image:: _static/ss3.png
   :width: 500px
   :height: 300px
   :align: center

- Avans əlavə et
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/"
    - Avans əlavə etmək json-da üçün göndərilməli olan datalar:
        - "employee_id" -> required, işçi id - User
            - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
        - "note" -> nullable, qeyd - String
        - "date" -> required, tarix - Date
        - "amount" -> nullable, "məbləğ" - float
            - Avans 2 formada verilir, əgər məbləğ daxil edilərsə məbləğə görə verilir, daxil edilməzsə yekun balansdan 15 faiz çıxılır. Hər işçi ay ərzində 2 dəfə avans ala bilir. Məbləğ daxil edilmədikdə toplam 30% avans ala bilir.
        - Avans əməliyyatı zamanı kassadan pul çıxılır.

.. code:: json

  {
    "employee_id": 18,
    "note": "test",
    "date": "01-11-2022",
    "amount": 100
  }

- Bütün avanslara bax
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/"
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "date" -> tarix - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

.. image:: _static/ss5.png
   :width: 300px
   :height: 200px
   :align: center


- Filter:
    - "http://localhost:8000/api/v1/salaries/advancepayment/?employee=1&year=2022&month=11"
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə avans axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"

- Avans sil
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, əks halda Ödənilmiş məbləği silə bilməyəcəyiniz ilə bağlı xəta mesajı alacaqsınız

+-----+
|Bonus|
+-----+

Bonus
-----

.. image:: _static/ss6.png
   :width: 400px
   :height: 30px
   :align: center

.. image:: _static/ss7.png
   :width: 500px
   :height: 300px
   :align: center

- Bonus əlavə et
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus/"
    - Bonus əlavə etmək json-da üçün göndərilməli olan datalar:
            - "employee_id" -> required, işçi id - User
                - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
            - "note" -> nullable, qeyd - String
            - "date" -> required, tarix - Date
            - "amount" -> required, "məbləğ" - float

.. code:: json

  {
    "employee_id": 69,
    "amount": 100,
    "note": "test",
    "date": "17-11-2022"
  }

- Bütün bonuslara bax
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus/"
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "date" -> tarix - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

.. image:: _static/ss8.png
   :width: 300px
   :height: 200px
   :align: center


- Filter:
    - "http://localhost:8000/api/v1/salaries/bonus/?employee=1&year=2022&month=11"
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə bonus axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"

- Bonus sil
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, əks halda Ödənilmiş məbləği silə bilməyəcəyiniz ilə bağlı xəta mesajı alacaqsınız

+------+
|Cərimə|
+------+

Cərimə
------

.. image:: _static/ss9.png
   :width: 400px
   :height: 30px
   :align: center

.. image:: _static/ss10.png
   :width: 500px
   :height: 300px
   :align: center

- Cərimə əlavə et
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/"
    - Cərimə əlavə etmək json-da üçün göndərilməli olan datalar:
            - "employee_id" -> required, işçi id - User
                - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
            - "note" -> nullable, qeyd - String
            - "date" -> required, tarix - Date
            - "amount" -> required, "məbləğ" - float

.. code:: json

  {
    "employee_id": 69,
    "amount": 100,
    "note": "test",
    "date": "17-11-2022"
  }

- Bütün cərimələrə bax
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/"
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "date" -> tarix - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

.. image:: _static/ss11.png
   :width: 300px
   :height: 200px
   :align: center


- Filter:
    - "http://localhost:8000/api/v1/salaries/salary-punishment/?employee=1&year=2022&month=11"
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə cərimə axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"

- Cərimə sil
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, əks halda Ödənilmiş məbləği silə bilməyəcəyiniz ilə bağlı xəta mesajı alacaqsınız

+-------+
|Kəsinti|
+-------+

Kəsinti
-------

.. image:: _static/ss12.png
   :width: 400px
   :height: 30px
   :align: center

.. image:: _static/ss13.png
   :width: 500px
   :height: 300px
   :align: center

- Kəsinti əlavə et
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/"
    - Kəsinti əlavə etmək json-da üçün göndərilməli olan datalar:
            - "employee_id" -> required, işçi id - User
                - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
            - "note" -> nullable, qeyd - String
            - "date" -> required, tarix - Date
            - "amount" -> required, "məbləğ" - float

.. code:: json

  {
    "employee_id": 69,
    "amount": 100,
    "note": "test",
    "date": "17-11-2022"
  }

- Bütün Kəsintilərə bax
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/"
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "date" -> tarix - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

.. image:: _static/ss14.png
   :width: 300px
   :height: 200px
   :align: center


- Filter:
    - "http://localhost:8000/api/v1/salaries/salary-deduction/?employee=1&year=2022&month=11"
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə Kəsinti axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"

- Kəsinti sil
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, əks halda Ödənilmiş məbləği silə bilməyəcəyiniz ilə bağlı xəta mesajı alacaqsınız

+--------+
|Ə/H Ödə |
+--------+

Ə/H Ödə
-------

- Əməkhaqqı ödəmək
    - endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/"
    - Json daxilində göndəriləcək data:
        - "employee" -> required. işçi id - User
        - "note" -> nullable. qeyd - String
        - "date" -> required. tarix - Date. hansı tarixin maaşı ödənilməsi istənilirsə həmin tarix. Yəni əgər bu ay ödənəcəksə prosesin edildiyi tarix göndərilə bilər, backend üçün lazım olan ordakı il və aydır. Günün neçə daxil edilməsi önəmli deyil.
    - Əməkhaqqı ödəmək əməliyyatı zamanı kassadan pul çıxılır və həmin tarixdə verilmiş bonus, kəsinti və cərimələr ödəndi statusuna keçir.

.. code:: json

  {
    "employee": 21,
    "note": "maas odemek",
    "date": "01-10-2022"
  }

- Bütün əməkhaqqı ödəmə əməliyyatlarına bax
    - endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/"
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "date" -> tarix - Date
        - "salary_date" -> maaşın ödənilmə tarixi - Date
        - "amount" -> ödənilmiş məbləğ - float

.. image:: _static/ss17.png
   :width: 300px
   :height: 200px
   :align: center

- Filter
    - endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/?employee__fullname=&employee__fullname__icontains=&employee__id=&employee__id__icontains=&employee__position__name=&employee__position__name__icontains=&employee__employee_status__status_name=&employee__employee_status__status_name__icontains=&amount=&amount__gte=&amount__lte=&note=&note__icontains=&date=&date__gte=&date__lte=&year=&month="

- İD-ə görəə əməkhaqqı ödəmə əməliyyatına bax
    - endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/1/"