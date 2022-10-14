###################
Contract (Müqavilə)
###################

- group_leader 
      - nullable, gonderilmmir. 
      - avtomatik login olan user qeyd olunur backend terefinden (User)
- manager1_id 
      - nullable 
      - (menecer1 - User id)
- manager2_id 
      - nullable 
      - (menecer2 - User id)
- customer_id 
      - required 
      - (müştəri - Customer id)
- product_id 
      - required 
      - (məhsul - Product id)
- product_quantity 
      - Eger gonderilmese avtomatik 1 qebul edilir. 
      - (məhsul sayı - int)
- total_amount 
      - gonderilmir, backend terefinde hesablanib verilir. 
      - (ümumi məbləğ - float)
- electronic_signature 
      - required 
      - (imza - file)
- contract_date 
      - nullable 
      - (müqavilə tarixi - datefield)
- contract_created_date 
      - gonderilmir, backend terefinden muqavilenin imzalandigi gun avtomatik qeyd olunur 
      - (datefield)
- company 
      - nullable. Gonderilmir, login olan userin shirketi goturulur avtomatik. 
      - (şirkət - Shirket)
- office 
      - nullable. Eger ofisi olmayan terefinden imazalanirsa muqavile mutleq ofis gonderilmelidir. 
      - (ofis - Ofis)
- remaining_debt 
      - gonderilmir, backend-de avtomatik hesablanir 
      - (qalıq borc - Float)
- is_remove 
      - Sokunut emeliyyati zamani true olaraq gonderilir 
      - (Boolean)
- payment_style 
      - required 
      - (müqavilə növü - Enum[String] = (Nəğd, Kredit))
- new_graphic_amount 
      - nullable Yeni qrafik prosesində göndərilir 
      - (yeni qrafik məbləği - Float)
- new_graphic_status 
      - nullable Yeni qrafik prosesində göndərilir 
      - (yeni qrafik statusu - String (YENİ QRAFİK))
- modified_product_status 
      - nullable, mehsul deyisdirilmesi zamani gonderilir 
      - (String)
- contract_status 
      - required 
      - (muqavile_status - String)
- loan_term 
      - Ancaq kredit ile olan muqavilelerde gonderilir 
      - (kredit_muddeti - int)
- initial_payment 
      - nullable
      -  Ancaq kredit ile olan muqavilelerde gonderilir 
      - (ilkin_odenis - float)
- initial_payment_debt 
      - nullable
      - Ancaq kredit ile olan muqavilelerde gonderilir 
      - (ilkin_odenis_qaliq - float)
- initial_payment_date 
      - nullable
      - Ancaq kredit ile olan muqavilelerde gonderilir 
      - (ilkin_odenis_tarixi - datefield)
- initial_payment_debt_date
      - nullable
      - Ancaq kredit ile olan muqavilelerde gonderilir 
      - (ilkin_odenis_qaliq_tarixi - datefield)
- pdf 
      - nullable, backend terefinden avtomatik create olunur 
      - (file)
- pdf2
      - nullable, backend terefinden avtomatik create olunur 
      - (file)
- cancelled_date
      - nullable, muqavile dusen zaman avto hemin tarix goturulur. Isteye gore manual gonderile bilinir 
      - (dusme_tarixi - datefield)
- debt_closing_date
      - nullable. Borc baglandi statusuna kecirilen zaman gonderilir, gonderilmese avtomatik hemin tarixi secir. 
      - (borc_baglanma_tarixi - datefield)
- compensation_income
      - nullable 
      - (kompensasiya_medaxil - float)
- compensation_expense
      - nullable 
      - (kompensasiya_mexaric - float)
- debt_finished
      - Gonderilmir, borc baglanan zaman avtomatik True olur 
      - (borc_baglandi - boolean)
- note 
      - nullable. 
      - (qeyd - Text)

=====

+----------------+
|Contract create |
+----------------+

Contract create
---------------

- endpoint: "http://localhost:8000/api/v1/contract/"
- Müqavilə create edərkən, əgər müqaviləni create edən user admindirsə, bu zaman mütləq ofis_id daxil etməlidir. Yox əgər vanleader və ya ofis-i olan hər hansı başqa userdirsə bu zaman json içərisində ofis_id göndərməyə ehtiyac yoxdur, çünki avtomatik olaraq həmin user-in ofisi götürüləcək.
- Cash contract

.. code:: json

  {
    "manager1_id": ,
    "manager2_id": ,
    "customer_id": ,
    "product_id": ,
    "office_id": ,
    "product_quantity": ,
    "electronic_signature": ,
    "contract_date": ,
    "note": ,
    "payment_style": ,
  }

- Installment contract

.. code:: json

  {
    "manager1_id": ,
    "manager2_id": ,
    "customer_id": ,
    "product_id": ,
    "office_id": ,
    "product_quantity": ,
    "electronic_signature": ,
    "contract_date": ,
    "loan_term": ,
    "initial_payment": ,
    "initial_payment_debt": , // Əgər ikinci ilkin ödəniş olmayacaqsa jsonda göndərilmir
    "initial_payment_date": ,
    "initial_payment_debt_date": , // Əgər ikinci ilkin ödəniş olmayacaqsa jsonda göndərilmir
    "note": ,
    "payment_style": ,
  }


+-----------------+
|Get All Contract |
+-----------------+

Get All Contract
----------------

- endpoint: "http://localhost:8000/api/v1/contract/"


+-------------------+
|Get Contract By ID |
+-------------------+

Get Contract By ID
------------------

- endpoint: "http://localhost:8000/api/v1/contract/1/"


+--------------------------+
|Operations about Contract |
+--------------------------+

Operations about Contract
-------------------------

- endpoint: "http://localhost:8000/api/v1/contract/1/"

**New Graphic (Yeni Qrafik)**

.. code:: json

  {
    "new_graphic_amount": 100, // hər ay nə qədər məbləğ ödəmək istədiyini bildirir və cari məbləğdən az olmalıdır.
    "new_graphic_status": "YENİ QRAFİK"
  }

**Kreditli müqavilədə ilkin ödənişlərin ödənməsi**

- 1-ci ilkin ödənişin ödənilməsi.

---------------------------------

.. code:: json

  {
    "initial_payment": 100
  }

- 2-ci ilkin ödənişin ödənilməsi.

---------------------------------

.. code:: json

  {
    "initial_payment_debt": 100
  }

**Müqaviləni düşən statusuna keçirtmək -- SÖKÜNTÜ**

- Müqaviləni düşən statusuna keçirdərkən, əgər müştəriyə kompensasiya ödənənəcəksə compensation_expense fieldinə ödənəcək məbləğ daxil edilir və bu məbləğ ofis kassasından avtomatik çıxılır
- Müqaviləni düşən statusuna keçirdərkən, əgər müştəridən kompensasiya alınacaqsa compensation_income fieldinə alınacaq məbləğ daxil edilir və bu məbləğ ofis kassasına avtomatik əlavə edilir
- Müqaviləni düşən statusuna keçirdərkən, əgər kompensasiya ilə bağlı əməliyyat edilməyəcəksə compensation_income və compensation_expense null göndərilir.
- compensation_income və compensation_expense eyni anda göndərilmir, xəta mesajı backend tərəfindən veriləcək.
- Bu proses zamanı məhsul anbara qaytarılır. Və bu müqavilədən işçilərə verilən kommisiyalar geri alınır.

.. code:: json

  {
    "contract_status": "DÜŞƏN",
    "compensation_income": null, 
    "compensation_expense": 100,
    "note": ""
  }

**Müqaviləni düşən statusundan davam edən statusuna keçirtmək**

- Bu proses zamanı məhsul anbardan yenidən çıxılır
- servislər və kreditlər tarixə əsasən yenidən müəyyən edilir

.. code:: json

  {
    "contract_status": "DAVAM EDƏN"
  }


+-------------------------------+
|Müqaviləyə hədiyyə təyin etmək |
+-------------------------------+

Müqaviləyə hədiyyə təyin etmək
------------------------------

**müqaviləyə hədiyyə təyin etmək**

- endpoint: "http://localhost:8000/api/v1/contract/gifts/"

.. code:: json

  {
    "product_id": null, // mütləq null göndərilməlidir.
    "contract_id": 1,
    "products_and_quantity": "3-5,4-6" // "hədiyyə_məhsul1_id-sayı,hədiyyə_məhsul2_id-sayı"
  }

**müqavilədən hədiyyəni silmək**

- hədiyyəni silmək üçün aşağıdakı endpointə delete sorğusu göndərilir.
- endpoint: "http://localhost:8000/api/v1/contract/gifts/1/"

**müqaviləyə təyin olunmuş hədiyyələrə baxmaq**

- hədiyyəni silmək üçün aşağıdakı endpointə delete sorğusu göndərilir.
- endpoint: "http://localhost:8000/api/v1/contract/gifts/1/"

**müqavilədən hədiyyəni silmək**

- hədiyyəni silmək üçün aşağıdakı endpointə delete sorğusu göndərilir.
- endpoint: "http://localhost:8000/api/v1/contract/gifts/1/"


+--------------------------------+
|Müqaviləyə kreditor təyin etmək |
+--------------------------------+

Müqaviləyə kreditor təyin etmək
-------------------------------

**müqaviləyə kreditor təyin etmək**

- endpoint: "http://localhost:8000/api/v1/contract/creditors/"

.. code:: json

  {
    "contract_id": null,
    "creditor_id": null
  }

**kreditorlara baxmaq**

- endpoint: "http://localhost:8000/api/v1/contract/creditors/"

**müqaviləyə təyin olunmuş kreditora id-sinə görə baxmaq**

- endpoint: "http://localhost:8000/api/v1/contract/creditors/1/"



+--------+
|Dəyişim |
+--------+

Dəyişim
-------

**Dəyişim**

- endpoint: "http://localhost:8000/api/v1/contract/change-product-of-contract/"
- Bütün fieldlar required-dır

.. code:: json

  {
    "payment_style": "KREDİT",
    "loan_term": 10,
    "old_contract": 72,
    "product": 8,
    "note": ""
  }


+-----------------------------------------------------+
|Müqavilə imzalanmamış aylara düşən məbləğlərə baxmaq |
+-----------------------------------------------------+

Müqavilə imzalanmamış aylara düşən məbləğlərə baxmaq
----------------------------------------------------

**Müqavilə imzalanmamış aylara düşən məbləğlərə baxmaq**

- endpoint: "http://localhost:8000/api/v1/contract/test-installment/"
- Bütün fieldlar required-dır, 

.. code:: json

  {
    "loan_term":10,
    "product_quantity":10,
    "payment_style":"KREDİT",
    "contract_date":"14-10-2022",
    "initial_payment":100,
    "initial_payment_debt":0,
    "product_id":1,
  }
