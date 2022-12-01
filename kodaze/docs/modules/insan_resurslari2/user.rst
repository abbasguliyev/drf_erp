############
User (İşçi)
############

- username
    - create prosesinde gonderilmir
    - backend-de avtomatik user-{last_user_id+1} formasinda create olunur. 
    - (Istifadəçi adı - String)
- fullname 
    - required. 
    - Mutleq gonderilmelidir, ad soyad ata adi. 
    - (Adı Soyadı Ata adı - String)
- start_date_of_work 
    - nullable. 
    - Null gonderilerse avtomatik bu gunki tarixi verir. 
    - (İşə başlama tarixi - Date)
- dismissal_date 
    - nullable. 
    - Isci deaktiv edildikde avtomatik deaktiv edildiyi tarix dusur. 
    - (İşdən ayrılma tarixi - Date)
- phone_number_1 
    - required.  
    - (Telefon1 - String)
- phone_number_2 
    - nullable 
    - (Telefon2 - String)
- photo_ID 
    - required, 
    - mutleq gonderilmelidir 
    - (Şəxsiyyət vəsiqəsi - File)
- back_photo_of_ID 
    - nullable    
    - (Şəxsiyyət vəsiqəsi 2- File)
- driving_license_photo 
    - nullable 
    - (Sürücülük vəsiqəsi - File)
- company
    - nullable, create prosesi zamanı göndərilmir. Avtomatik Alliance Holding seçilir.
    - (Holdinq - Holdinq id)
- company
    - nullable 
    - (Şirkət - Company id)
- department 
    - nullable 
    - (Departament - Department id)
- office
    - nullable 
    - (Ofis - Office id)
- section 
    - nullable
    - (Şöbə - Section id) 
    - Dizaynda yığışdırılıb(Göndərilmir)
- position 
    - nullable 
    - (Vəzifə - Position id)
- team
    - nullable 
    - (Team - Team id) 
    - Dizaynda yığışdırılıb(Göndərilmir)
- employee_status 
    - nullable 
    - (İşçi statusu - Section id) 
    - Dizaynda yığışdırılıb(Göndərilmir)
- user_permissions 
    - nullable 
    - (İcazə - Permission id) 
    - Create zamanı lazım deyil, Update zamanı istifadə edilir
- groups
    - nullable 
    - (İcazə Qrupu - Group id) 
    - Create zamanı lazım deyil, Update zamanı istifadə edilir
- profile_image 
    - nullable 
    - (Profil şəkli - File)
- register_type 
    - required 
    - (Müqavilə növü - Enum[String]("xidməti müqavilə", "əmək müqaviləsi"))
- salary_style
    - required 
    - (Ə/H ödəmə üslubu - Enum[String]("aylıq", "günlük", "həftəlik", "fix"))
- salary
    - nullable 
    - (Ə/H - Float)
- supervizor 
    - nullable 
    - (Supervizor - User id)
- commission
    - nullable
    - (Komissiya id - Commission id)
- note 
    - nullable 
    - (Qeyd - String)
- password 
    - required

=====

+-----+
|Login|
+-----+

Login
-----

- login endpoint : "http://localhost:8000/api/v1/users/login/"

- Authorization type : Bearer

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
    "register_type": "",
    "salary_style": "",
    "salary": null,
    "supervisor": null,
    "commission": null,
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
    "company_id": null,
    "department_id": null,
    "office_id": null,
    "section_id": null,
    "position_id": null,
    "employee_status_id": null,
    "user_permissions_id": [],
    "groups_id": [],
    "profile_image": null,
    "register_type": "",
    "salary_style": "",
    "salary": null,
    "supervisor": null,
    "commission_id": null,
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

Get User of Company
-------------------

- endpoint: "http://localhost:8000/api/v1/users/?company__name=Ocean"
- endpoint: "http://localhost:8000/api/v1/users/?company=1"

Get User of Holding
-------------------

- endpoint: "http://localhost:8000/api/v1/users/?holding__name=Alliance"
- endpoint: "http://localhost:8000/api/v1/users/?holding=1"

+----------------+
|Deactivate User |
+----------------+

Deactivate User
---------------

- endpoint: "http://localhost:8000/api/v1/users/1/"

- User-i deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı  database-dən silmir. Sadəcə is_active fieldini False edir.