#####################
TaskRequest (Tarixçə)
#####################

- "creator"
    - tapşırığı daxil edəni bildirir
    - Avtomatik create olunduğu üçün json-da göndərilmir
    - (Tapşırıq verən - User)
- "note"
    - required
    - (Səbəb - String)
- "new_date"
    - required.
    - (Yeni Tarix - Date)
- "task"
    - required
    - (Hansı Tapşırığa göndərilir - TaskManager İD)
- "change_date"
    - dəyişmə tarixi, avtomatik create olduğu üçün json-da göndərilmir
    - (dəyişmə tarixi - Date)
- "is_accept"
    - default False, ancaq təsdiqlə etdikdə göndərilməlidir. Tarixçənin təsdiq edildiyini bildirir. Create prosesində göndərilmir, avtomatik backend-də False olaraq düşür.
    - (İcazə ver/vermə - Boolean)

=====

+-------------------+
|TaskRequest create |
+-------------------+

TaskRequest create
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/task-request/"

.. code:: json

  {
    "note": "test",
    "new_date": "16-09-2022",
    "task": 1
  }

+-------------------+
|Update TaskRequest |
+-------------------+

Update TaskRequest
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/task-request/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "note": "test",
    "new_date": "16-09-2022",
    "task": 1,
    "is_accept": true
  }

+--------------------+
|Get All TaskRequest |
+--------------------+

Get All TaskRequest
-------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/task-request/"


+----------------------+
|Get TaskRequest By ID |
+----------------------+

Get TaskRequest By ID
---------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/task-request/1/"

+-------------------+
|Delete TaskRequest |
+-------------------+

Delete TaskRequest
------------------

- endpoint: "http://localhost:8000/api/v1/task-manager/task-request/1/"