######
Backup
######

- Backup və restore proseslərini etmək üçün boş json ilə post sorğusu atılır

=====

+-------+
|Backup |
+-------+

Backup
------

- endpoint: "http://localhost:8000/api/v1/backup/"

+--------+
|Restore |
+--------+

Restore
-------

- endpoint: "http://localhost:8000/api/v1/backup/restore/"

+-------------+
|Media Backup |
+-------------+

Media Backup
------------

- endpoint: "http://localhost:8000/api/v1/backup/media-backup/"


+-----------+
|Get Backup |
+-----------+

Get Backup
----------

- endpoint: "http://localhost:8000/api/v1/backup/get-backup/"

.. code:: json

  {
    "id": 1,
    "backup_date": "10-10-2022",
    "restore_date": null,
    "media_backup_date": null
  }
