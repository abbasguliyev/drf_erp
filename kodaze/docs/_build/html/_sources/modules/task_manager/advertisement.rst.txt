####################
Advertisement (Elan)
####################

- "creator"
    - tapşırığı daxil edəni bildirir
    - Avtomatik create olunduğu üçün json-da göndərilmir
    - (Tapşırıq verən - User)
- "title"
    - required
    - (başlıq - String)
- "body"
    - required.
    - (tərkibi - String)
- "created_date"
    - nullable, (Əgər null olarsa avtomatik bu gün seçiləcək)
    - (başlama tarixi - Date)
- "position"
    - required, əgər vəzifə seçilməyəcəksə [] formasında boş list göndərilir
    - (tapşırığın verildiyi vəzifələr - Position List

=====

+---------------------+
|Advertisement create |
+---------------------+

Advertisement create
--------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/"
- position gonderilerken [id_1, id_2] formasinda gonderilmelidir. Eger bir id gonderilecekse [id_1] seklinde olmalidir. Əgər vəzifə göndərilməyəcəksə [] formasında yazılmalıdır

.. code:: json

  {
    "title": "test",
    "body": "test",
    "created_date": null,
    "position_id": []
  }

+---------------------+
|Update Advertisement |
+---------------------+

Update Advertisement
--------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "title": "test",
    "body": "test",
    "created_date": null,
    "position_id": []
  }

+----------------------+
|Get All Advertisement |
+----------------------+

Get All Advertisement
---------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/"


+------------------------+
|Get Advertisement By ID |
+------------------------+

Get Advertisement By ID
-----------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"

+---------------------+
|Delete Advertisement |
+---------------------+

Delete Advertisement
--------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"