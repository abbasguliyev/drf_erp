#################
Kassa Hərəkətləri
#################

+-----------------+
|Kassa Hərəkətləri|
+-----------------+

Kassa Hərəkətləri
-----------------

.. image:: _static/ss33.png
   :width: 1000px
   :height: 250px
   :alt: melumat
   :align: center

.. image:: _static/ss34.png
   :width: 1000px
   :height: 250px
   :alt: melumat
   :align: center

- Jsonda gələn data:
    - date - (Tarix - Date)
    - description - nullable, (Açıqlama - String)
    - operation_style - (Əməliyyat növü - Enum<String>["MƏDAXİL", "MƏXARİC"])
    - quantity - (miqdar - Float)
    - customer - nullable, (Müştəri - Customer)
    - personal - (Personal - User)
    - company - nullable, (Company - Şirkət)
    - office - nullable, (Office - Ofis)
    - initial_balance - (İlkin balans - Float)
    - subsequent_balance - (Sonrakı balans - Float)
    - holding_initial_balance - (Holdinq İlkin balans - Float)
    - holding_subsequent_balance - (Holdinq Sonrakı balans - Float)
    - company_initial_balance - (Şirkət İlkin balans - Float)
    - company_subsequent_balance - (Şirkət Sonrakı balans - Float)
    - office_initial_balance - (Ofis İlkin balans - Float)
    - office_subsequent_balance - (Ofis Sonrakı balans - Float)

.. image:: _static/ss35.png
   :width: 1500px
   :height: 250px
   :alt: melumat
   :align: center


- Bütün Kassa Hərəkətləri
    - endpoint: "http://localhost:8000/api/v1/cashbox/cashflow/"

- Filter
    - endpoint: "http://localhost:8000/api/v1/cashbox/cashflow/?executor=&executor__fullname=&executor__fullname__icontains=&executor__position__name=&executor__position__name__icontains=&executor__employee_status__status_name=&executor__employee_status__status_name__icontains=&holding__name=&holding__name__icontains=&holding=&office__name=&office__name__icontains=&office=&company__name=&company__name__icontains=&company=&initial_balance=&initial_balance__gte=&initial_balance__lte=&subsequent_balance=&subsequent_balance__gte=&subsequent_balance__lte=&description=&description__icontains=&operation_style=&operation_style__icontains=&date=&date__gte=&date__lte="

- İd-ə görə Kassa Hərəkətləri
    - endpoint: "http://localhost:8000/api/v1/cashbox/cashflow/1/"

+----------------+
|Şirkət Əməliyyat|
+----------------+

Şirkət Əməliyyat
----------------

.. image:: _static/ss36.png
   :width: 1000px
   :height: 200px
   :alt: melumat
   :align: center

- Şirkət Əməliyyatı etmək
    - endpoint: "http://localhost:8000/api/v1/cashbox/company-cashbox-operation/"
    - Json-da göndərilməli olan datalar:
        - "company_id" -> required, Şirkət id - Company İD
            - şirkət endpointi: "http://localhost:8000/api/v1/company/?is_active=true"
        - "office_id" -> nullable, Ofis id - Office İD
            - əgər daxil edilməzsə əməliyyat şirkət kassasına ediləcək, daxil edilərsə isə ofis kassasına ediləcək
            - ofis endpointi: "http://localhost:8000/api/v1/company/offices/?company=&company__id=&company__name=&company__name__icontains=&is_active=true"
        - "amount" -> required, məbləğ - float
        - "note" -> nullable, qeyd - string
        - "operation" -> required, əməliyyat növü (MƏDAXİL, MƏXARİC)
        - "personal_id" -> nullable, İşçi - User id, mühasibin əməliyyat apardığı işçidir.
            - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"

.. code:: json

  {
    "company_id": 4,
    "office_id": 2,
    "amount": 150,
    "note": null,
    "operation": "MƏDAXİL",
    "personal_id": null
  }

+-----------------+
|Holdinq Əməliyyat|
+-----------------+

Holdinq Əməliyyat
-----------------

.. image:: _static/ss38.png
   :width: 1500px
   :height: 350px
   :alt: melumat
   :align: center

- Holdinq Əməliyyatı etmək
    - endpoint: "http://localhost:8000/api/v1/cashbox/holding-cashbox-operation/"
    - Json-da göndərilməli olan datalar:
        - "amount" -> required, məbləğ - float
        - "note" -> nullable, qeyd - string
        - "operation" -> required, əməliyyat növü (MƏDAXİL, MƏXARİC)
        - "personal_id" -> nullable, İşçi - User id, mühasibin əməliyyat apardığı işçidir.
            - işçilərin enpointi: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"

.. code:: json

  {
    "personal_id": null,
    "amount": 1000,
    "note": "test",
    "operation": "MƏDAXİL"
  }
