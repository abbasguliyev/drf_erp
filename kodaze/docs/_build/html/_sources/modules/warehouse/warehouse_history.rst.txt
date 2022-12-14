###############
Anbar Tarixçəsi
###############

+----------------+
|Anbar Tarixçəsi |
+----------------+

Anbar Tarixçəsi
---------------

- Bütün anbar tarixçələrinə baxmaq
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-history/"
    - Jsonda gələn data
        - "id" - id-si - int
        - "company" - Əməliyyatın baş verdiyi şirkət - Json
        - "customer" - Satış prosesi zamanı hansı müştəriyə məhsulun satıldığını bildirir - Json
        - "executor" - Cari əməliyyatı icra edən personalı bildirir - Json
        - "date" - tarix
        - "sender_warehouse" - Anbar əməliyyat zamanı çıxış edilən anbar - string
        - "receiving_warehouse" - Məhsulu qəbul edən anbarı - string
        - "sender_previous_quantity" - Çıxış anbarda məhsulun əməliyyatdan öncəki miqdarı - int
        - "sender_subsequent_quantity" - Çıxış anbarda məhsulun əməliyyatdan sonrakı miqdarı - int
        - "recepient_previous_quantity" -  Qəbul edən anbarda məhsulun əməliyyatdan öncəki miqdarı - int
        - "recepient_subsequent_quantity" - Qəbul edən anbarda məhsulun əməliyyatdan sonrakı miqdarı - int
        - "product" - Əməliyyat zamanı istifadə edilən məhsulun adı - string
        - "quantity" - Əməliyyat zamanı istifadə edilən məhsulun miqdarı - int
        - "operation_style" - Əməliyyatın növü - string - (Transfer, Giriş, Utilizasiya, Yeniləmə, Servis, Söküntü, Dəyişim, Satış)
        - "note" - Əməliyyat ilə bağlı daxil edilən qeydləri bildirir

- Filter
    - endpoint "http://localhost:8000/api/v1/warehouse/warehouse-history/?customer=&customer__fullname=&customer__fullname__icontains=&company=&sender_warehouse=&receiving_warehouse=&operation_style=&executor=&date=&date__gte=&date__lte=&phone_number="

- Filter zamanı çıxış və giriş anbarları dropdown olaraq veriləcəksə bu zaman aşağıdakı url-ə sorğu ataraq dropdown-da anbarların adlarını qeyd edin.
- Daha sonra isə &sender_warehouse=&receiving_warehouse= filterlərinə bu urldən gələn responsdakı name-ləri mənimsədərək axtarış edə bilərsiniz.