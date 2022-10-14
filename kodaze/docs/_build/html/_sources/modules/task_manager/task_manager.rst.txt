#########################
TaskManager (Tapşırıqlar)
#########################

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
- "end_date"
    - required
    - (bitmə tarixi - Date)
- "old_date"
    - göndərilmir, (Bitm' tarixi yeniləndiyi zaman avtomatik əvvəki bitmə tarixi old tarix olur.)
    - (köhnə tarix - Date)
- "users"
    - nullable, ancaq create zamanı lazımdır.
    - (tapşırığın verildiyi əməkdaşlar - String (Necə göndərilməsi ilə bağlı create bölməsinə baxın))
- "positions"
    - nullable, ancaq create zamanı lazımdır.
    - (tapşırığın verildiyi vəzifələr - String (Necə göndərilməsi ilə bağlı create bölməsinə baxın))
- "employee_id"
    - nullable (Ancaq get və put sorğusunda lazımdır, create zamanı istifadə olunmur)
    - İşçi İD - User İD
- "position_id"
    - nullable (Ancaq get və put sorğusunda lazımdır, create zamanı istifadə olunmur)
    - Vəzifə İD - Position İD

=====

+-------------------+
|TaskManager create |
+-------------------+

TaskManager create
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/"
- users ve ya positions gonderilerken "id_1, id_2" formasinda gonderilmelidir. 
- Eger bir id gonderilecekse "id_1" seklinde olmalidir. users datasi gonderilerse positions null gonderilmelidir, positions gonderilerse users null gonderilmelidir.

.. code:: json

  {
    "title": "test",
    "body": "test",
    "created_date": null,
    "end_date": "11-10-2022",
    "users": "1",
    "positions": null,
    "position_id": null, // Bu 2 field mütləq null göndərilməlidir.
    "employee_id": null  // Bu 2 field mütləq null göndərilməlidir. 
  }

+-------------------+
|Update TaskManager |
+-------------------+

Update TaskManager
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "title": "test",
    "body": "test",
    "created_date": null,
    "end_date": "11-10-2022",
    "employee": 1,
    "position": null,
    "status": "Tamamlandı",
    "position_id": null,
    "employee_id": null 
  }

+--------------------+
|Get All TaskManager |
+--------------------+

Get All TaskManager
-------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/"


+----------------------+
|Get TaskManager By ID |
+----------------------+

Get TaskManager By ID
---------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"

+-------------------+
|Delete TaskManager |
+-------------------+

Delete TaskManager
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/1/"