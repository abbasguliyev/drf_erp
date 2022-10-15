####################
Installment (Kredit)
####################

- month_no 
      - Ay nömrəsi - int
- contract 
      - (müqavilə - Contract)
- price 
      - məbləğ - float
- payment_status 
      - (ödəmə statusu - String["ÖDƏNMƏYƏN", "ÖDƏNƏN"])
- conditional_payment_status 
      - (şərtli ödəmə statusu - String["BURAXILMIŞ AY", "NATAMAM AY", "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ", "ARTIQ ÖDƏMƏ", "SON AYIN BÖLÜNMƏSİ"])
- close_the_debt_status 
      - (borc bağla statusu - String["BORCU BAĞLA"])
- delay_status 
      - (gecikdirmə statusu - String["GECİKDİRMƏ"])
- missed_month_substatus 
      - (buraxılmış ay statusu - String["SIFIR NÖVBƏTİ AY", "SIFIR SONUNCU AY", "SIFIR DİGƏR AYLAR"])
- incomplete_month_substatus 
      - (natamam ay statusu - String["NATAMAM NÖVBƏTİ AY", "NATAMAM SONUNCU AY", "NATAMAM DİGƏR AYLAR"])
- overpayment_substatus 
      - (artıq ödəmə statusu - String["ARTIQ BİR AY", "ARTIQ BÜTÜN AYLAR"])
- last_month 
      - (son ay - Boolean)
- note 
      - (qeyd - String)

=====

+-----------------------+
|Installment Operations |
+-----------------------+

Installment Operations
----------------------

+--------------------+
|Get All Installment |
+--------------------+

Get All Installment
-------------------

- endpoint: "http://localhost:8000/api/v1/contract/installments/"


+----------------------+
|Get Installment By ID |
+----------------------+

Get Installment By ID
---------------------

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"

**BORCU BAĞLA ILE BAGLI EMELIYYATLAR**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"

.. code:: json

  {
    "close_the_debt_status": "BORCU BAĞLA"
  }

**GECIKDIRME ILE BAGLI EMELIYYATLAR**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"

.. code:: json

  {
    "delay_status": "GECİKDİRMƏ",
    "date": "18-11-2022"
  }

**Natamam Ay odeme statusu ile bagli əməliyyat**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"
- price cari məbləğdən az olmalıdır

- Natamam digər aylar

----

.. code:: json

  {
    "conditional_payment_status": "NATAMAM AY",
    "incomplete_month_substatus": "NATAMAM DİGƏR AYLAR",
    "price": 50
  }

- NATAMAM NÖVBƏTİ AY

----

.. code:: json

  {
    "conditional_payment_status": "NATAMAM AY",
    "incomplete_month_substatus": "NATAMAM NÖVBƏTİ AY",
    "price": 50
  }

- NATAMAM SONUNCU AY

----

.. code:: json

  {
    "conditional_payment_status": "NATAMAM AY",
    "incomplete_month_substatus": "NATAMAM SONUNCU AY",
    "price": 50
  }

**Buraxilmis Ay odeme statusu ile bagli əməliyyat**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"
- price hər zaman 0 olmalıdır.

- SIFIR DİGƏR AYLAR

----

.. code:: json

  {
    "conditional_payment_status": "BURAXILMIŞ AY",
    "missed_month_substatus": "SIFIR DİGƏR AYLAR",
    "price": 0
  }

- SIFIR NÖVBƏTİ AY

----

.. code:: json

  {
    "conditional_payment_status": "BURAXILMIŞ AY",
    "missed_month_substatus": "SIFIR NÖVBƏTİ AY",
    "price": 0
  }

- SIFIR SONUNCU AY

----

.. code:: json

  {
    "conditional_payment_status": "BURAXILMIŞ AY",
    "missed_month_substatus": "SIFIR SONUNCU AY",
    "price": 0
  }

**RAZILASDIRILMIS AZ ODEME ile bagli əməliyyat**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"
- Razılaşdırılmış ödəmə statusunda ödənmək istənilən məbləğ (price) cari məbləğdən az olmalıdır
- Razılaşdırılmış az ödəmə məbləği digər aylar arasında bərabər paylaşdırır.

.. code:: json

  {
    "conditional_payment_status": "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ",
    "price": 150
  }

**ARTIQ ODEME ile bagli əməliyyat**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"
- Artıq ödəmə statusunda ödənmək istənilən məbləğ (price) cari məbləğdən çox olmalıdır

- ARTIQ BİR AY
- Bu status məbləği sonuncu aydan çıxır

----

.. code:: json

  {
    "conditional_payment_status": "ARTIQ ÖDƏMƏ",
    "overpayment_substatus": "ARTIQ BİR AY",
    "price": 200
  }

- ARTIQ BÜTÜN AYLAR

----

.. code:: json

  {
    "conditional_payment_status": "ARTIQ ÖDƏMƏ",
    "overpayment_substatus": "ARTIQ BÜTÜN AYLAR",
    "price": 200
  }

**SON AYIN BOLUNMESI**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"

----

.. code:: json

  {
    "conditional_payment_status": "SON AYIN BÖLÜNMƏSİ",
    "price": 200
  }

**Odenen ay ile bagli emeliyyat**

- endpoint: "http://localhost:8000/api/v1/contract/installments/1/"
- Price cari məbləğə bərabər olarsa kredit ödənmiş olur.

----

.. code:: json

  {
    "price": 200
  }
