########
Anbarlar
########

+---------+
|Anbarlar |
+---------+

Anbarlar
--------

- Bütün anbarlara bax
    - endpoint: "http://localhost:8000/api/v1/warehouse/"
    - Ofis əlavə edildikdə, həmin ofis üçün avtomatik olaraq anbar qurulur. Proses backenddə baş verir. 
    - Get sorğusundan sonra response içərində gələn data:
        - "id" -> anbarın id-si - int
        - "company" -> anbarın aid olduğu şirkət - Json
            - "id" -> şirkətin id-si - int
            - "name" -> şirkətin adı - string
        - "office" -> anbarın aid olduğu ofis - Json
            - "id" -> ofisin id-si - int
            - "name" -> ofisin adı - string
            - "company" -> ofisin aid olduğu şirkət - Json
                - "id" -> şirkətin id-si - int
                - "name" -> şirkətin adı - string
        - "name" -> Anbarın adı - string
        - "is_active" -> anbarın aktiv olub olmadığını bildirir. (true/false) - Boolean

    - Filter
        - endpoint "http://localhost:8000/api/v1/warehouse/?name=&name__icontains=&is_active=unknown&office=&company="

- anbarı id-sinə görə axtarmaq
    - endpoint: "http://localhost:8000/api/v1/warehouse/1/"

+--------------+
|Holding Anbar |
+--------------+

Holding Anbar
-------------

- Bütün holding anbar məhsullarına bax
    - endpoint: "http://localhost:8000/api/v1/warehouse/holding-warehouse/"
    - Response-da results listi içərisində 2 json gəlir. extra və data.
    - Response-da gələn extra:
        - "all_quantity" - ümumi miqdarın cəmini bildirir.
        - "all_useful_product_count" - istifadəyə yararlı məhsulların miqdarının cəmini bildirir
        - "all_unuseful_product_count" - istifadəyə yararsız məhsulların miqdarının cəmini bildirir
        - "all_price" - məhsulların qiymətinin cəmini bildirir.
    - Response-da gələn data:
        - "id" -> anbarın id-si - int
        - "product" -> məhsul - Json
            - "id" - məhsulun id-si - int 
            - "category" - məhsulun kateqoriyası - Json
                - "id" - kateqoriyanın id-si - int
                - "category_name" - kateqoriyanın adı - string
            - "unit_of_measure" - məhsulun ölçü vahidi - Json
                - "id" - ölçü vahidinin id-si - int
                - "name" - ölçü vahidinin adı - string
            - "product_name" - məhsulun adı - string
            - "barcode" - məhsulun barcode-u - int
            - "purchase_price" - məhsulun alış qiyməti - float
            - "price" - məhsulun satış qiyməti - float
            - "guarantee" - zəmanət(ay) - int
            - "is_gift" - hədiyyə - boolean
            - "weight" - çəkisi - float
            - "width" - eni - float
            - "length" - uzunluğu - float
            - "height" - hündürlüyü - float
            - "volume" - həcmi - float
            - "note" - qeyd - string
            - "product_image" - məhsulun şəkli - İmage
        - "quantity" - miqdarı - int
        - "useful_product_count" - yararlı məhsulların miqdarı - int
        - "unuseful_product_count" - yararsız məhsulların miqdarı - int

- Holding anbar məhsulunu id-sinə görə axtar
    - endpoint: "http://localhost:8000/api/v1/warehouse/holding-warehouse/1/"

- Filter
    - endpoint "http://localhost:8000/api/v1/warehouse/holding-warehouse/?product=&product__product_name=&product__product_name__icontains=&product__barcode=&product__barcode__icontains=&quantity=&useful_product_count=&unuseful_product_count="

- Holding anbarına məhsul əlavə etmək
    - endpoint: "http://localhost:8000/api/v1/warehouse/product-add-to-holding-warehouse/"
    - Jsonda göndərilməli olan data
        - "product_name" - required - məhsulun adı - string
        - "barcode" - məhsulun barcode-u - int
        - "category" - məhsulun kategoriya id-si - int
            - kateqoriyalar üçün endpoint - "http://localhost:8000/api/v1/product/categories/"
        - "unit_of_measure" - məhsulun ölçü vahidinin id-si - int
            - ölçü vahidləri üçün endpoint - "http://localhost:8000/api/v1/product/unit-of-measure/"
        - "purchase_price" - məhsulun alış qiyməti - float
        - "price" - məhsulun satış qiyməti - float
        - "guarantee" - zəmanət(ay) - int
        - "is_gift" - hədiyyə - boolean
        - "weight" - çəkisi - float
        - "width" - eni - float
        - "length" - uzunluğu - float
        - "height" - hündürlüyü - float
        - "volume" - həcmi - float
        - "note" - qeyd - string
        - "product_image" - məhsulun şəkli - İmage
        - "quantity" - miqdarı - int

- holding anbarındakı məhsulu update etmək
    - endpoint "http://localhost:8000/api/v1/warehouse/holding-warehouse-update/3/"
    - Update üçün put sorğusu göndəriləcək. Amma put sorğusu patch kimi işləyir.Yəni fieldlar tək-tək və ya toplu şəkildə göndərilə bilinir.
    - Jsonda göndəriləcək datalar
        - "product_name" - məhsulun adı - string
        - "barcode" - məhsulun barcode-u - int
        - "category" - məhsulun kategoriya id-si - int
            - kateqoriyalar üçün endpoint - "http://localhost:8000/api/v1/product/categories/"
        - "unit_of_measure" - məhsulun ölçü vahidinin id-si - int
            - ölçü vahidləri üçün endpoint - "http://localhost:8000/api/v1/product/unit-of-measure/"
        - "purchase_price" - məhsulun alış qiyməti - float
        - "price" - məhsulun satış qiyməti - float
        - "guarantee" - zəmanət(ay) - int
        - "is_gift" - hədiyyə - boolean
        - "weight" - çəkisi - float
        - "width" - eni - float
        - "length" - uzunluğu - float
        - "height" - hündürlüyü - float
        - "volume" - həcmi - float
        - "note" - qeyd - string
        - "product_image" - məhsulun şəkli - İmage
        - "quantity" - miqdarı - int

- Utilizasiya
    - endpoint "http://localhost:8000/api/v1/warehouse/change-unuseless-product/"
    - Jsonda göndəriləcək data
        - "products_and_quantity" - required - utilizasiya edilməsini istədiyiniz məhsullar və sayı
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan silinməsi istənilən holding anbar məhsulunun id-sidir. defisdən sağda yazılan isə silinməsi istənilən saydır.
                - Holding anbar məhsullarının id-si üçün endpoint: "http://localhost:8000/api/v1/warehouse/holding-warehouse/". Burdan holding warehouse id-sini götürürük. Qeyd - bu endpointə  sorğu atanda həm təkcə id datası gəlir, həmdə product datası və onun içində id datası gəlir. Bizə lazım olan tək id datasıdır. 1-ci sıradakı.
        - "note" - Qeyd
