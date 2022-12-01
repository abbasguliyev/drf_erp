######################
Commission (Komissiya)
######################

- "commission_name"
    - required
    - (Komissiya adı - String)
- "for_office"
    - nullable.
    - (Ofisə görə - Float)
    - Ofisin satışına görə komissiya veriləcəksə bu hissədə yazılır.
- "cash"
    - nullable
    - (Nəğd - Float)
    - Nəğd müqavilələrdə komissiya veriləcəksə bu hissədə yazılır.
- "for_team"
    - nullable
    - (komandaya görə - Float)
    - Komandanın satışına görə komissiya veriləcəksə bu hissədə yazılır.
- "creditor_per_cent"
    - nullable
    - (kreditor - int)
    - Müqaviləyə təyin olunmuş kreditorun neçə faiz komissiya alacağını təyin edir.
    - Kreditor komissiyası bu hissədə yazılır.
- "month_ranges"
    - nullable
    - (kredit aralığı - Create və update zamanı göndərilir. String olaraq göndərilməlidir)
    - "month_range_id-məbləğ" formasında göndərilməlidir.
    - Dizayndakı kredit aralığı hissəsindəki 2-3, 4-12 MonthRange table-dan get sorğusu ilə gəlməlidir.
        Əvvəlcə MonthRange əlavə edilməlidir. MonthRange ay aralıqlarını bildirir.
        Necə əlavə edildiyinə dokumentasiyadan baxa bilərsiniz. məbləğ isə dizaynda 2-3, 4-12 və s. qarşısında
        yazılacaq məbləğdir. Məsələn ilk öncə 2-3 ay aralığı seçildi, id-sinin 1 olduğunu fərz edək
        və məbləğ olaraq 180 yazıldı.
        Bu zaman json-da 2-3 month range id-sini və məbləği "1-180" olaraq göndəririk.
- "sale_ranges"
    - nullable
    - (Satış sayı aralığı - Create və update zamanı göndərilir. String olaraq göndərilməlidir)
    - "sale_range_id-məbləğ-fix(və ya say)" formasında göndərilməlidir.
    - Dizayndakı satış sayı aralığı hissəsindəki 2-3, 4-12 SaleRange table-dan get sorğusu ilə gəlməlidir.
        Əvvəlcə SaleRange əlavə edilməlidir. SaleRange satış ay aralıqlarını bildirir.
        Necə əlavə edildiyinə dokumentasiyadan baxa bilərsiniz. məbləğ isə dizaynda 2-3, 4-12 və s. qarşısında
        yazılacaq məbləğdir. fix və say isə məbləğdən sonra seçiləndir, statikdir,
        Məsələn ilk öncə 2-3 ay aralığı seçildi, id-sinin 1 olduğunu fərz edək
        və məbləğ olaraq 180 yazıldı, fix və say seçildi.
        Bu zaman json-da 2-3 month range id-sini, məbləği və fix(əgər say seçilibsə say) "1-180-fix"(və ya "1-180-say")
        olaraq göndəririk.


=====

+------------------+
|Commission create |
+------------------+

Commission create
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/commission/"

.. code:: json

  {
    "commission_name": "Commission of Canvasser",
    "for_office": null,
    "cash": 160,
    "for_team": null,
    "month_ranges": "1-160,2-140,3-120,4-100",
    "sale_ranges": "1-150-fix,2-250-say",
    "creditor_per_cent": null
  }

+------------------+
|Update Commission |
+------------------+

Update Commission
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/commission/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir
- Xatırlatma => month_ranges ay aralığı, sale_ranges satış sayı ararlığı üçündür
- month_ranges və sale_ranges create-də olduğu kimi göndərilir, bütün month_ranges və sale_ranges
    update olunub olunmamağından asılı olmayaraq göndərilməlidir. Yeni month_ranges və sale_ranges
    əlavə olunacaqsa belə hamısı yenə göndərilməlidir, backenddə update və yeni data əlavəsi avtomatik gedir.
- month_ranges üçün get sorğusunda installment fieldinə baxın
- sale_ranges üçün get sorğusunda for_sale_range fieldinə baxın.

.. code:: json

  {
    "commission_name": "Commission of Canvasser",
    "for_office": 500,
    "cash": 160,
    "for_team": 200,
    "month_ranges": "1-160,2-140,3-120,4-100",
    "sale_ranges": "1-150-fix,2-250-say",
    "creditor_per_cent": 50
  }

+-------------------+
|Get All Commission |
+-------------------+

Get All Commission
------------------

- endpoint: "http://localhost:8000/api/v1/salaries/commission/"


+---------------------+
|Get Commission By ID |
+---------------------+

Get Commission By ID
--------------------

- endpoint: "http://localhost:8000/api/v1/salaries/commission/1/"

+------------------+
|Delete Commission |
+------------------+

Delete Commission
-----------------

- endpoint: "http://localhost:8000/api/v1/salaries/commission/1/"