#########
Əməkhaqqı
#########

+-----------------+
|Əməkhaqqı cədvəli|
+-----------------+

Əməkhaqqı cədvəli
-----------------

- Response-da extra və data deyə 2 məlumat gəlir. 
    - data içində yazılan normal response datalarıdır. 
    - extra içində isə bəzi dataların ümumi toplamı gəlir. Əməkhaqqı cədvəlində extra içində gələn datalar aşağıdakılardır:
        - "all_bonus" -> Responseda gələn bütün toplam bonusları ifadə edir,
        - "all_advancepayment" -> Responseda gələn bütün toplam avansları ifadə edir,
        - "all_salarydeduction" -> Responseda gələn bütün toplam kəsintiləri ifadə edir,
        - "all_salarypunishment" -> Responseda gələn bütün toplam cərimələri ifadə edir,
        - "all_final_salary" -> Responseda gələn bütün toplam yekun maaşları ifadə edir,
        - "all_working_day" -> Responseda gələn bütün toplam iş günlərini ifadə edir,
        - "all_const_salary" -> Responseda gələn bütün toplam sabit ə/h-ları ifadə edir,
        - "all_sale_quantity" -> Responseda gələn bütün toplam satış saylarını ifadə edir,
        - "all_commission" -> Responseda gələn bütün toplam komisiyyaları ifadə edir
    - extra içindəki datalar, pagination və filterləməyə uyğun çalışır.

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
    - "http://localhost:8000/api/v1/salaries/salary-views/?employee=&employee__fullname=&employee__fullname__icontains=&employee__is_superuser=unknown&employee__salary_style=&employee__office=&employee__office__id=&employee__office__name=&employee__office__name__icontains=&employee__company=&employee__company__id=&employee__company__name=&employee__company__name__icontains=&employee__position=&employee__position__id=&employee__position__name=&employee__position__name__icontains=&employee__register_type=&employee__register_type__icontains=&employee__employee_status=&employee__employee_status__status_name=&employee__employee_status__status_name__icontains=&is_done=unknown&sale_quantity=&sale_quantity__gte=&sale_quantity__lte=&sales_amount=&sales_amount__gte=&sales_amount__lte=&final_salary=&final_salary__gte=&final_salary__lte=&date=&date__month=&date__year=&date__gte=&date__lte="

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
        - "date" -> əməliyyatın icrası zamanı daxil edilən tarix - Date
        - "salary_date" -> əməliyyatın aparıldığı ə/h cədvəlinin tarixi - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

- Filter:
    - "http://localhost:8000/api/v1/salaries/advancepayment/?employee=1&salary_date__month=&salary_date__year="
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə avans axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.


- Avans sil
    - endpoint: "http://localhost:8000/api/v1/salaries/advancepayment/1/"
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, əks halda Ödənilmiş məbləği silə bilməyəcəyiniz ilə bağlı xəta mesajı alacaqsınız

+-----+
|Bonus|
+-----+

Bonus
-----

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
        - "date" -> əməliyyatın icrası zamanı daxil edilən tarix - Date
        - "salary_date" -> əməliyyatın aparıldığı ə/h cədvəlinin tarixi - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

- Filter:
    - "http://localhost:8000/api/v1/salaries/bonus/?employee=1&salary_date__month=&salary_date__year="
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə bonus axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus/1/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.

- Bonus sil
    - endpoint: "http://localhost:8000/api/v1/salaries/bonus-delete/"
    - Silmək istədiyiniz bonusların list şəklində jsonda `instance_list` -ə yazırsınız və post sorğusu ilə qeyd edilmiş url-ə göndərirsiniz.
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, Front end tərəfdə validasiyası qoyulmalıdır
    - Nümunə:

.. code:: json

 {
    "instance_list": [70, 71]
 }

+------+
|Cərimə|
+------+

Cərimə
------

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
        - "date" -> əməliyyatın icrası zamanı daxil edilən tarix - Date
        - "salary_date" -> əməliyyatın aparıldığı ə/h cədvəlinin tarixi - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

- Filter:
    - "http://localhost:8000/api/v1/salaries/salary-punishment/?employee=1&salary_date__month=&salary_date__year="
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə cərimə axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment/1/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.

- Cərimə sil
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction-delete/"
    - Silmək istədiyiniz cərimələri list şəklində jsonda `instance_list` -ə yazırsınız və post sorğusu ilə qeyd edilmiş url-ə göndərirsiniz.
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, Front end tərəfdə validasiyası qoyulmalıdır
    - Nümunə:

.. code:: json

 {
    "instance_list": [70, 71]
 }

+-------+
|Kəsinti|
+-------+

Kəsinti
-------

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
        - "date" -> əməliyyatın icrası zamanı daxil edilən tarix - Date
        - "salary_date" -> əməliyyatın aparıldığı ə/h cədvəlinin tarixi - Date
        - "amount" -> "məbləğ" - float
        - "is_paid" -> "status" - Boolean, Ödənilib ödənilmədiyini bildirir.

- Filter:
    - "http://localhost:8000/api/v1/salaries/salary-deduction/?employee=1&salary_date__month=&salary_date__year="
    - year və month-a salary view içərisində gələn date-in year və month məlumatları verilməlidir.

- İD-ə görə Kəsinti axtar
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-deduction/1/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.

- Kəsinti sil
    - endpoint: "http://localhost:8000/api/v1/salaries/salary-punishment-delete/"
    - Silmək istədiyiniz kəsintiləri list şəklində jsonda `instance_list` -ə yazırsınız və post sorğusu ilə qeyd edilmiş url-ə göndərirsiniz.
    - Silmə əməliyyatı yalnız ödənilməmiş məbləğlər üçün keçərlidir, Front end tərəfdə validasiyası qoyulmalıdır
    - Nümunə:

.. code:: json

 {
    "instance_list": [70, 71]
 }

+--------+
|Ə/H Ödə |
+--------+

Ə/H Ödə
-------

- Əməkhaqqı ödəmək
    - endpoint: "http://localhost:8000/api/v1/salaries/pay-salary/"
    - Json daxilində göndəriləcək data:
        - "salary_view" -> required. Ə/H id - SalaryView ID
    - Ə/H cədvəlindən ödənilməsi istənilən əməkhaqqılar seçilir və onların id-ləri json-da göndərilir
    - Əməkhaqqı ödəmək əməliyyatı zamanı kassadan pul çıxılır və həmin tarixdə verilmiş bonus, kəsinti və cərimələr ödəndi statusuna keçir.

.. code:: json

  {
    "salary_view": [396,398]
  }
