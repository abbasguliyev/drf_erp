#############
Ödəniş izləmə
#############

+-------------+
|Ödəniş izləmə|
+-------------+

Ödəniş izləmə
-------------

- Ödəniş izləmə
    - endpoint: "http://localhost:8000/api/v1/contract/installments/"
    - Json-da gələn datalar
        - date - ödəmə tarixi
        - contract - müqavilə
            - customer - müştəri
                - fullname - adı soyadı ata adı
                - region - şəhər, bölgə
            - company - şirkət
            - office - ofis
            - remaining_debt - qalıq borc
        - price - ödəyəcəyi məbləğ
        - pay_status_helper - ödəmə statusu
            - ["ÖDƏNMƏYƏN","ÖDƏNƏN","BURAXILMIŞ AY","NATAMAM AY","RAZILAŞDIRILMIŞ AZ ÖDƏMƏ","ARTIQ ÖDƏMƏ","SON AYIN BÖLÜNMƏSİ"]
        - contract_creditor - kreditor    

- Filter
    - endpoint: "http://localhost:8000/api/v1/contract/installments/?contract=&contract__office=&contract__company=&contract__creditors__creditor=&contract__creditors__creditor__fullname=&contract__customer=&contract__customer__fullname=&contract__customer__fullname__icontains=&contract__customer__region=&pay_status_helper=&pay_status_helper__icontains=&date=&date__gte=&date__lte="