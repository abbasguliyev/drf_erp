##################
Customer (Müştəri)
##################

- "region_id"
    - required 
    - (şəhər - Region id)
- "fullname"
    - required (
    - Ad Soyadı Ata adı - String)
- "email"
    - nullable 
    - (email - email field-string kimidir sadəcə @ işarəsi mütləq olmalıdır)
- "profile_image"
    - nullable 
    - (Profil şəkli - File)
- "photo_ID"
    - nullable 
    - (Şəxsiyyət vəsiqəsi ön hissə - File)
- "back_photo_of_ID"
    - nullable 
    - (Şəxsiyyət vəsiqəsi arxa hissə - File)
- "phone_number_1"
    - required 
    - (Telefon nömrəsi 1 - String)
- "phone_number_2"
    - nullable 
    - (Telefon nömrəsi 1 - String)
- "phone_number_3"
    - nullable 
    - (Telefon nömrəsi 1 - String)
- "phone_number_4"
    - nullable 
    - (Telefon nömrəsi 1 - String)
- "address"
    - required 
    - (ünvan - String)
- "note"
    - nullable 
    - (qeyd - Textarea)
- "is_active"
    - Boolean. 
    - Create zamanı göndərilmir, default olaraq True olur. Update zamanı isə dəyişilə bilinir



=====

+-----------------+
|Get all customers|
+-----------------+

Get all customers
-----

- endpoint : "http://localhost:8000/api/v1/users/customers/"

.. code:: json

  {
    "username": "admin",
    "password": "admin123"
  }

+--------------+
|Token Refresh |
+--------------+

Token Refresh
-------------

- endpoint : http://127.0.0.1:8000/api/v1/users/token-refresh/

.. code:: json

  {
    "refresh": "refresh token bura qeyd edilir. Refresh token login zamani elde edilir"
  }

+---------------------------+
|Change Login User Password |
+---------------------------+

Change Login User Password
--------------------------

- endpoint : http://127.0.0.1:8000/api/v1/users/change-password/

.. code:: json

  {
    "old_password": "",
    "new_password": ""
  }


+--------------------------------------------------------------------+
|Changing the user's password by the admin according to the username |
+--------------------------------------------------------------------+

Changing the user's password by the admin according to the username
-------------------------------------------------------------------

- endpoint : http://127.0.0.1:8000/api/v1/users/change-password/

.. code:: json

  {
    "username": "abbasguliyev",
    "new_password": "admin-123"
  }


+------------------+
|User Registration |
+------------------+

User Registration
-----------------

- register endpoint: "http://localhost:8000/api/v1/users/register/"

.. code:: json

  {
    "fullname": "",
    "start_date_of_work": null,
    "dismissal_date": null,
    "phone_number_1": "",
    "phone_number_2": "",
    "photo_ID": null,
    "back_photo_of_ID": null,
    "driving_license_photo": null,
    "company": null,
    "department": null,
    "office": null,
    "section": null,
    "position": null,
    "employee_status": null,
    "user_permissions": [],
    "groups": [],
    "profile_image": null,
    "contract_type": "",
    "salary_style": "",
    "salary": null,
    "supervisor": null,
    "note": "",
    "password": ""
  }

+-------------+
|Update Users |
+-------------+

Update Users
------------

- endpoint: "http://localhost:8000/api/v1/users/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "username": "",
    "fullname": "",
    "start_date_of_work": null,
    "dismissal_date": null,
    "phone_number_1": "",
    "phone_number_2": "",
    "photo_ID": null,
    "back_photo_of_ID": null,
    "driving_license_photo": null,
    "company": null,
    "department": null,
    "office": null,
    "section": null,
    "position": null,
    "employee_status": null,
    "user_permissions": [],
    "groups": [],
    "profile_image": null,
    "contract_type": "",
    "salary_style": "",
    "salary": null,
    "supervisor": null,
    "note": "",
    "is_active": "",
  }

+--------------+
|Get All Users |
+--------------+

Get All Users
-------------

- endpoint: "http://localhost:8000/api/v1/users/"


+---------------+
|Get User By ID |
+---------------+

Get User By ID
--------------

- endpoint: "http://localhost:8000/api/v1/users/1/"

+----------------+
|Deactivate User |
+----------------+

Deactivate User
---------------

- endpoint: "http://localhost:8000/api/v1/users/1/"

- User-i deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı  database-dən silmir. Sadəcə is_active fieldini False edir.