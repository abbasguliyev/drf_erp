####
Stok
####

+------+
|Stock |
+------+

Stock
-----

- Bütün stok dataları
    - endpoint: "http://localhost:8000/api/v1/warehouse/stocks/"
    - Response-da results listi içərisində 2 json gəlir. extra və data.
    - Response-da gələn extra:
        - "all_quantity" - ümumi miqdarın cəmini bildirir.
        - "all_useful_product_count" - istifadəyə yararlı məhsulların miqdarının cəmini bildirir
        - "all_changed_product_count" - Dəyişilmiş/Söküntü məhsulların miqdarının cəmini bildirir
    - Response-da gələn data:
        - "id" - stokun id-si - int
        - "warehouse" - stokun aid olduğu anbar - Json
            - "id" - anbarın id-si - int
            - "name" - anbarın adı - string
        - "product" - məhsul - Json
            - "id" - id-si - int
            - "product_name" - məhsulun adı - string
            - "price" - qiyməti - float
        - "useful_product_count" - yararlı məhsulların sayı - int
        - "quantity" - ümumi say - int
        - "changed_product_count" - dəyişilmiş/sökülmüş məhsulların sayı - int
        - "date" - stok əlavə edilmə tarixi - date
        - "note" - qeyd - string

- Filter
    - endpoint "http://localhost:8000/api/v1/warehouse/stocks/?product=&product__product_name=&product__product_name__icontains=&product__price=&product__price__gte=&product__price__lte=&product__barcode=&product__barcode__gte=&product__barcode__lte=&warehouse__company=&warehouse=&product__is_gift=unknown"

- id-yə görə stok axtarmaq
    - endpoint: "http://localhost:8000/api/v1/warehouse/stocks/1/"

- stok silmək
    - endpoint: "http://localhost:8000/api/v1/warehouse/stocks/1/"

Transferlər
-----------

- Holding -> Ofis transfer
    - endpoint "http://localhost:8000/api/v1/warehouse/holding-to-office-product-transfer/"
    - Jsonda göndəriləcək data
        - "products_and_quantity" - required - məhsul idləri və sayları
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan göndəriləcək holding anbar məhsulunun id-sidir. defisdən sağda yazılan isə göndəriləcək saydır.
                - Holding anbar məhsullarının id-si üçün endpoint: "http://localhost:8000/api/v1/warehouse/holding-warehouse/". Burdan holding warehouse id-sini götürürük. Qeyd - bu endpointə  sorğu atanda həm təkcə id datası gəlir, həmdə product datası və onun içində id datası gəlir. Bizə lazım olan tək id datasıdır. 1-ci sıradakı.
        - "company" - required - şirkət id
            - şirkət idlərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/"
        - "warehouse" - required - ofis id
            - fieldin adı warehouse olsa da burda ofisin id-si göndəriləcək. Zatən hər ofisin yalnız bir anbarı olur.
            - ofis id-lərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/offices/"

- Ofislər arası transfer
    - endpoint "http://localhost:8000/api/v1/warehouse/between-office-product-transfer/"
    - Jsonda göndəriləcək data
        - "company" - required - şirkət id
            - şirkət idlərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/"
        - "sender_office" - required - göndərən ofis id
            - ofis id-lərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/offices/"
        - "recipient_office" - required - qəbul edən ofis id
            - ofis id-lərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/offices/"
        - "products_and_quantity" - required - məhsul idləri və sayları
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan göndəriləcək məhsulunun id-sidir. defisdən sağda yazılan isə göndəriləcək saydır.
                - Göndərən ofisin anbarındakı məhsullarının id-si üçün endpoint: "http://localhost:8000/api/v1/warehouse/stocks/?warehouse__office=1". Burdan product datasının id-sini götürürük. Qeyd - bu endpointə  sorğu atanda həm təkcə id datası gəlir, həmdə product datası və onun içində id datası gəlir. Bizə lazım olan productun id datasıdır
        - "note" - qeyd

- Ofis -> Holding transfer
    - endpoint "http://localhost:8000/api/v1/warehouse/office-to-holding-product-transfer/"
    - Jsonda göndəriləcək data
        - "products_and_quantity" - required - məhsul idləri və sayları
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan göndəriləcək məhsulunun id-sidir. defisdən sağda yazılan isə göndəriləcək saydır.
                - Göndərən ofisin anbarındakı məhsullarının id-si üçün endpoint: "http://localhost:8000/api/v1/warehouse/stocks/?warehouse__office=1". Burdan product datasının id-sini götürürük. Qeyd - bu endpointə  sorğu atanda həm təkcə id datası gəlir, həmdə product datası və onun içində id datası gəlir. Bizə lazım olan productun id datasıdır
        - "company" - required - şirkət id
            - şirkət idlərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/"
        - "warehouse" - required - ofis id
            - fieldin adı warehouse olsa da burda ofisin id-si göndəriləcək. Zatən hər ofisin yalnız bir anbarı olur.
            - ofis id-lərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/offices/"
