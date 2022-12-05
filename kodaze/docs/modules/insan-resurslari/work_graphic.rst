##########
İş qrafiki
##########

+----------+
|İş qrafiki|
+----------+

İş qrafiki Cədvəli
------------------

- Response-da extra və data deyə 2 məlumat gəlir. 
    - data içində yazılan normal response datalarıdır. 
    - extra içində isə bəzi dataların ümumi toplamı gəlir. Əməkhaqqı cədvəlində extra içində gələn datalar aşağıdakılardır:
        - "all_working_day_count" -> Responseda gələn bütün toplam iş günlərini ifadə edir,
        - "all_const_salary" -> Responseda gələn bütün toplam sabit ə/h-ları ifadə edir,
        - "all_holiday" -> Responseda gələn bütün toplam tətil günlərini ifadə edir,
        - "all_payed_days_off" -> Responseda gələn bütün toplam ödənişli icazələri ifadə edir,
        - "all_unpayed_days_off" -> Responseda gələn bütün toplam ödənişsiz icazələri ifadə edir
    - extra içindəki datalar, pagination və filterləməyə uyğun çalışır.

- İş qrafiki Cədvəli
    - endpoint "http://localhost:8000/api/v1/holidays/employee-working-days/"
    - Json-da gələn data:
        - "employee": İşçi
            - "company": sabit ə/h
            - "office": sabit ə/h
            - "position": sabit ə/h
            - "username": Istifadəçi adı
            - "fullname": Ad soyad ata adı
            - "salary": sabit ə/h
        - "extra_data":
            - "total_holiday": Tətil Günü sayı
            - "total_payed_days_off": Ödənişli icazə günü sayı
            - "total_unpayed_days_off": Ödənişsiz icazə günü sayı
        - "working_days_count": İş günü sayı
        - "date": Cədvəlin aid olduğu tarix

- Filter:
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-working-days/?employee=&employee__fullname=&employee__fullname__icontains=&employee__company=&employee__office=&employee__position=&employee__register_type=&employee__register_type__icontains=&date=&date__month=&date__year=&date__gte=&date__lte="
    - filterdəki start_date və end_date date fieldinə görə hərəkət edir.

Tətil
-----

- Tətil əlavə et
    - endpoint: "http://localhost:8000/api/v1/holidays/holiday-operation/"
    - Tətil əlavə etmək json-da üçün göndərilməli olan datalar:
        - "person_on_duty_id":  Növbətçilər 
            - null göndərilə bilməz. Əgər növbətçi seçilməyəcəksə boş list göndərmək lazımdır.
            - User endpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
        - "company_id": Company İD
            - “Holding” seçildiyi zaman “Şirkət” və “Ofis” null göndərilir. Bu o
                deməkdir ki, tətil üçün seçilmiş günlər ancaq Holding personalına aiddir. “Holding” seçimi
                olmadığı təqdirdə isə Şirkət və Ofis seçimləri göndərilməlidir.
        - "office_id": Office İD
            - “Holding” seçildiyi zaman “Şirkət” və “Ofis” null göndərilir. Bu o
                deməkdir ki, tətil üçün seçilmiş günlər ancaq Holding personalına aiddir. “Holding” seçimi
                olmadığı təqdirdə isə Şirkət və Ofis seçimləri göndərilməlidir.
        - "holiday_date": Tətil günləri. Aşağıdakı nümunədə də göstərildiyi kimi dırnaq işarələri arasında yəni string formatında tətil edilməsi istənilən günlər seçilir və 
            işçilərin iş günləri sayı verilmiş tarixə uyğun olaraq azalır. Yəni Əgər string daxilində həm yanvar həm də fevral aylarından tətil günləri göndərilibsə bu zaman 
            işçinin uyğun olaraq yanvar ayındakı və fevral ayındakı iş günü sayı azalır. İş günlərinin sayı işçi register edildiyində avtomatik olaraq cari ay və növbəti ayın 
            günlərinin sayına görə 28, 29, 30, 31 olur. Hər ayın 1-i və 15i isə periodik olaraq növbəti aya uyğun iş günü sayı create olunur.
            - Nümunə: "holiday_date": "01-11-2022, 02-11-2022, 03-11-2022, 04-11-2022"
        - "holding": boolean. İşçinin holdingə aid olub olmadığını bildirir.
            - “Holding” seçildiyi zaman “Şirkət” və “Ofis” null göndərilir. Bu o
                deməkdir ki, tətil üçün seçilmiş günlər ancaq Holding personalına aiddir. “Holding” seçimi
                olmadığı təqdirdə isə Şirkət və Ofis seçimləri göndərilməlidir.

.. code:: json

  {
    "person_on_duty_id": [102,103],
    "company_id": 4,
    "office_id": 2,
    "holiday_date": "01-11-2022, 02-11-2022, 03-11-2022, 04-11-2022",
    "holding": false
  }

- Bütün Tətil tarixçələrinə bax
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-holiday-history/?employee=1&created_date=&created_date__gte=&created_date__lte="
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "day_count" -> Tətil günü sayı - İnt
        - "holiday_dates" -> Tətil günləri listi - List[String]
        - "created_date" -> Tarix - Date

- İD-ə görə Tətil tarixçəsi axtar
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-holiday-history/1/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.

- Tətil tarixçəsi sil
    - endpoint: "http://localhost:8000/api/v1/holidays/holiday-history-delete/"
    - Silmək istədiyiniz tətil tarixçələrinin id-lərini list şəklində jsonda `instance_list` -ə yazırsınız və post sorğusu ilə qeyd edilmiş url-ə göndərirsiniz.
    - Nümunə:

.. code:: json

 {
    "instance_list": [2,4]
 }

İcazə
-----

- İcazə əlavə et
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-day-off-operation/"
    - İcazələr ödənişli və ödənişsiz olmaq üzərə 2 yerə bölünür. Ödənişli icazələr yalnızca ə/h üslubu fix və fix+komissiya olan işçilər üçündür. 
        Bu zaman işçinin maaşını onun iş günü sayına bölüb alınan məbləği icazə gününü sayına vurub işçinin yekun maaşından çıxırıq. Proses backenddə baş verir.
    - İcazə əlavə etmək json-da üçün göndərilməli olan datalar:
            - "employee_id":  İcazə veriləcək işçilərin siyahısı. List şəklində seçilmiş işçilərin id-si göndərilməlidir
                - null göndərilə bilməz. Əgər növbətçi seçilməyəcəksə boş list göndərmək lazımdır.
                - User endpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
            - "day_off_date": İcazə günləri. Aşağıdakı nümunədə də göstərildiyi kimi dırnaq işarələri arasında yəni string formatında icazə tarixləri seçilir və 
                işçilərin iş günləri sayı verilmiş tarixə uyğun olaraq azalır. Yəni Əgər string daxilində həm yanvar həm də fevral aylarından icazə tarixləri göndərilibsə bu zaman 
                işçinin uyğun olaraq yanvar ayındakı və fevral ayındakı iş günü sayı azalır. İş günlərinin sayı işçi register edildiyində avtomatik olaraq cari ay və növbəti ayın 
                günlərinin sayına görə 28, 29, 30, 31 olur. Hər ayın 1-i və 15i isə periodik olaraq növbəti aya uyğun iş günü sayı create olunur.
                - Nümunə: "day_off_date": "01-11-2022, 02-11-2022, 03-11-2022, 04-11-2022"
            - "is_paid": boolean. 
                - İcazənin ödənişli olub olmadığını bildirir. True olarsa ödənişli, False olarsa isə ödənişsiz icazə create olacaq

.. code:: json

  {
    "employee_id": [105,106],
    "day_off_date": "03-12-2022,04-12-2022",
    "is_paid": true
  }

- Bütün İcazə tarixçələrinə bax
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-day-off-history/?employee=&created_date=&is_paid=unknown&created_date__gte=&created_date__lte="
    - Json-da gələn data:
        - "employee" -> işçi - User
        - "note" -> qeyd - String
        - "paid_day_count" -> Ödənişli İcazə günü sayı - İnt
        - "unpaid_day_count" -> Ödənişsiz İcazə günü sayı - İnt
        - "paid_days_off" -> Ödənişli İcazə günləri listi - List[String]
        - "unpaid_days_off" -> Ödənişsiz İcazə günləri listi - List[String]
        - "created_date" -> Tarix - Date
        - "is_paid": Ödənişlidirmi - Boolean 

- İD-ə görə İcazə tarixçəsi axtar
    - endpoint: "http://localhost:8000/api/v1/holidays/employee-day-off-history/3/"
    - update üçün Put sorğusu göndərmək lazımdır. Dəyişilməsini istədiyiniz fieldları tək tək və ya toplu şəkildə göndərmək olar. Update ancaq qeyd (note) fieldi üçün edilməlidir.

- İcazə tarixçəsi sil
    - endpoint: "http://localhost:8000/api/v1/holidays/day-off-history-delete/"
    - Silmək istədiyiniz icazə tarixçələrinin id-lərini list şəklində jsonda `instance_list` -ə yazırsınız və post sorğusu ilə qeyd edilmiş url-ə göndərirsiniz.
    - Nümunə:

.. code:: json

 {
    "instance_list": [2,4]
 }
