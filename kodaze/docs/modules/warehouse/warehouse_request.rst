###########
Anbar Sorğu
###########

+------------+
|Anbar sorğu |
+------------+

Anbar sorğu
-----------

- Bütün anbar sorğulara baxmaq
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/"
    - Jsonda gələn data
        - "id" - sorğunu id-si - int
        - "warehouse" - sorğunun göndərildiyi anbar - Json
            - "id" - anbarın id-si - int
            - "office" - anbarın aid olduğu ofis - Json
                - "id" - ofisin id-si - int
                - "name" - ofisin adı - string
                - "company" - ofisin aid olduğu şirkət - Json
                    - "id" - şirkətin id-si - int
                    - "name" - şirkətin adı - string
            - "name" - anbarın adı - string
        - "employee_who_sent_the_request" - sorğunu atan personal - Json
            - "id" - personalın idsi
            - "fullname" - personalın ad soyad ata adı
        - "products_and_quantities" - istənilən məhsullar və sayları - List
            - Listin içində gələn Json-ların içindəki datalar
                - "product_in_holding_warehouse_id" - məhsulun holding anbarındakı id-si, front end developerlər anbar sorğusunu icra edərkən bu id-dən istifadə edərək prosesi yerinə yetirə bilərlər. Əgər istənilən məhsul holding anbarında yoxdursa bu field null olacaq
                - "product_in_holding_warehouse_quantity" - məhsulun holding anbarındakı istifadəyə yararlı olanların miqdarı, front end developerlər anbar sorğusunu icra edərkən bu miqdardan istifadə edərək istənilən miqdarın anbarda olub olmadığını yoxlaya bilərlər. holding anbarına əlavə sorğu atmağa ehtiyac yoxdur. Əgər istənilən məhsul holding anbarında yoxdursa və ya istifadəyə yararlı məhsulun sayı 0 olarsa bu field 0 olacaq
                - "id" - məhsulun id-si
                - "product" - məhsulun adı
                - "quantity" - göndərilməsi istənilən say
        - "note" - qeyd - string
        - "status" - sorğunun icra vəziyyətini bildirən status - string 
            - Bu 3 haldan birində olur -> ["Yerinə Yetirilib", "Yerinə Yetirilməyib", "İmtina edildi"]
        - "request_date" - sorğunun göndərilmə tarixi - date
        - "execution_date" - sorğunun icra olunduğu tarix - date

- id-yə görə sorğu axtarmaq
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/1/"
  
- Filter
    - endpoint "http://localhost:8000/api/v1/warehouse/warehouse-requests/?note=&note__icontains=&warehouse__name=&warehouse__name__icontains=&warehouse__office__name=&warehouse__office__name__icontains="

- anbar sorğunu silmək
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/1/"

- Anbar sorğusu etmək
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests/"
    - Jsonda göndəriləcək data
        - "product_and_quantity"- required - məhsulların id-si və neçə dənə lazım olduqları
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan göndəriləcək məhsulunun id-sidir. defisdən sağda yazılan isə göndəriləcək saydır.
                - Məhsulların id-si üçün endpoint: "http://localhost:8000/api/v1/product/"
        - "note"- nullable- (Qeyd - String)

- Anbar sorğusunu icra etmək
    - endpoint: "http://localhost:8000/api/v1/warehouse/warehouse-requests-execute/4/"  /4 -> İcra edilməsi istənilən sorğunun id-sidir.
    - Jsonda göndəriləcək data
        - "product_and_quantity"- required - məhsulların id-si və neçə dənə lazım olduqları
            - json-da data aşağıdakı şəkildə göndərilməlidir
                - "3-100, 4-50, 5-100, 7-5000"
                - Burda defis işarəsindən solda yazılan göndəriləcək məhsulunun id-sidir. defisdən sağda yazılan isə göndəriləcək saydır.
                - Yuxarıda Bütün Anbar sorğuları üçün yazılmış dokumentasiyada products_and_quantities hissəsində holding anbarın id-sinin neçə olduğunun gəldiyi deyilib. Burda məhsulun id-si hissəsinə yəni defisdən sola o id-i yazılır
        - "company" - required - şirkət id
            - şirkət idlərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/"
        - "office" - required - ofis id
            - ofis id-lərini əldə etmək üçün endpoint "http://localhost:8000/api/v1/company/offices/"
        - "note" - nullable- (Qeyd - String)
        - "status" - required - sorğunun icra vəziyyətini bildirən status - string 
            - Bu 2 stringdən biri göndərilməlidir -> ["Yerinə Yetirilib", "İmtina edildi"]

        - Qeyd sorğunu icra etmək üçün post sorğusu göndərilməlidir. Əgər status İmtina edildi olaraq göndəriləcəksə Jsonda ancaq statusu göndərmək kifayətdir.