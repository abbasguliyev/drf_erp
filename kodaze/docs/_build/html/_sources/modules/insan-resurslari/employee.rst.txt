#######
İşçilər
#######

+-------+
|İşçilər|
+-------+

İşçilər
-------

- Login
    - endpoint "http://localhost:8000/api/v1/users/login/"
    - Authorization type : Bearer

.. code:: json

  {
    "username": "admin",
    "password": "admin123"
  }

- Token Refresh
    - endpoint : http://127.0.0.1:8000/api/v1/users/token-refresh/

.. code:: json

  {
    "refresh": "refresh token bura qeyd edilir. Refresh token login zamani elde edilir"
  }

- Şifrə Dəyiş
    - endpoint : http://localhost:8000/api/v1/users/password-reset/

.. code:: json

  {
    "username": "abbasguliyev",
    "new_password": "admin-123"
  }

- İşçi register etmək
    - endpoint "http://localhost:8000/api/v1/users/register/"
    - İşçi register edərkən username user-{userID} şəklində avtomatik create olur. Update bölməsindən dəyişə bilinir.
    - İşçilər 2 formada register edilir. Holding işçiləri və Şirkət işçiləri. register_type fieldində Şirkət və ya Holding seçilərək edilir.
        - Şirkət işçisi daxil ediliyi zaman mütləq Şirkət, Ofis dataları daxil edilməlidir
        - Holdinq işçisi daxil edildiyi zaman isə Şirkət və Ofis daxil edilməməlidir.
    - İşçi register etmək üçün json-da üçün göndərilməli olan datalar:
        - "register_type": required - String - Qeydiyyat növü [Şirkət, Holding]
        - "fullname": required - string - adı soyadı və ata adı
        - "phone_number_1": required - string - telefon nömrəsi
        - "phone_number_2": nullable - string - telefon nömrəsi
        - "region": nullable - Region İD - şəhəri
            - Region üçün endpoint: "http://localhost:8000/api/v1/users/region/"
        - "address": nullable - String - ünvanı
        - "email": nullable - String - e-poçt ünvanı
        - "company": nullable - Company İD - şirkəti
            - Şirkət üçün endpoint: "http://localhost:8000/api/v1/company/?is_active=true"
        - "office": nullable - Office İD - ofisi
            - Ofis üçün endpoint: "http://localhost:8000/api/v1/company/offices/?is_active=true"
        - "department": nullable - Department İD - departamenti
            - Department üçün endpoint: "http://localhost:8000/api/v1/company/departments/?is_active=true"
        - "supervisor": nullable - User İD - supervizoru
            - User üçün endpoint: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
        - "position": required - Position İD - vəzifəsi
            - Position üçün endpoint: "http://localhost:8000/api/v1/company/positions/?is_active=true"
        - "photo_ID": required - image - Şəxsiyyət vəsiqəsi(ön hissə)
        - "back_photo_of_ID": nullable - image - Şəxsiyyət vəsiqəsi(arxa hissə)
        - "driving_license_photo":  nullable - image - Sürücülük vəsiqəsi
        - "employee_status": nullable - EmployeeStatus İD - işçi statusu(Dizaynda hal-hazırda yığışdırılıb. Dizayndakı işçi statusu database-dən is_active olaraq gələn statusdur, register zamanı daxil edilmir, update və delete proseslərində lazım olacaq.)
            - EmployeeStatus üçün endpoint: "http://localhost:8000/api/v1/users/employee-status/"
        - "commission": nullable - Commission İD - Komissiya növü
            - Commission üçün endpoint: "http://localhost:8000/api/v1/salaries/commission/"
        - "salary_style": required - String - Ə/H növü [Fix, Fix+Kommissiya, Kommissiya]
        - "salary": nullable(Null göndərilsə də default 0 olur) - Float - Ə/H (AZN)
        - "note": nullable - String - Qeyd
        - "electronic_signature": required - image - İmza
        - "profile_image": nullable - image - Profil şəkli
        - "password": required - String - Şifrə

.. code:: json

  {
    "fullname": ,
    "phone_number_1": ,
    "phone_number_2": ,
    "region": ,
    "address": ,
    "email": ,
    "company": ,
    "office": ,
    "department": ,
    "supervisor": ,
    "position": ,
    "photo_ID": ,
    "back_photo_of_ID": ,
    "driving_license_photo": ,
    "employee_status": ,
    "commission": ,
    "salary_style": ,
    "salary": ,
    "note": ,
    "electronic_signature": ,
    "profile_image": ,
    "register_type": ,
    "password": 
  }

- İşçi update etmək
    - endpoint "http://localhost:8000/api/v1/users/2/"
    - Update zamanı Json-da göstərilən fieldlar tək tək və ya toplu şəkildə göndərilərək update prosesi yerinə yetirilir. Put sorğusu ilə göndərilir, ancaq patch sorğusu kimi fieldlar tək tək də göndərilə bilinir

- Json-da göndəriləcəklər:   
    - "company_id": Şirkət İD "http://localhost:8000/api/v1/company/?is_active=true",
    - "department_id": Department İD "http://localhost:8000/api/v1/company/departments/?is_active=true",
    - "office_id": Ofis İD "http://localhost:8000/api/v1/company/offices/?is_active=true",
    - "position_id": Vəzifə İD "http://localhost:8000/api/v1/company/positions/?is_active=true",
    - "employee_status_id": İşçi status İD "http://localhost:8000/api/v1/users/employee-status/",
    - "user_permissions_id": İcazə id-lər "http://localhost:8000/api/v1/users/permission-list/",
    - "groups_id": İcazə qrupları "http://localhost:8000/api/v1/users/all-permission-group/",
    - "commission_id": Komissiya İD "http://localhost:8000/api/v1/salaries/commission/",
    - "region_id": Bölgə İD "http://localhost:8000/api/v1/users/region/",
    - "is_superuser": false Boolean,
    - "username": İstifadəçi adı String,
    - "is_active": false Boolean,
    - "date_joined": Join tarixi Date,
    - "fullname": Ad soyad Ata adı String,
    - "phone_number_1": Telefon nömrəsi 1 String,
    - "phone_number_2": Telefon nömrəsi 2 String,
    - "address": Ünvan String,
    - "email": E-poçt String,
    - "photo_ID": Şəxsiyyət vəsiqəsi ön şəkli İmage,
    - "back_photo_of_ID": Şəxsiyyət vəsiqəsi arxa şəkli İmage,
    - "driving_license_photo": Sürücülük vəsiqəsi İmage,
    - "salary_style": ə/h üslubu String [Fix, Fix+Kommissiya, Kommissiya],
    - "salary": ə/h Float,
    - "note": qeyd String,
    - "electronic_signature": Elektron imza İmage,
    - "profile_image": Profil şəkli İmage,
    - "register_type": Qeydiyyat növü [Şirkət, Holding],
    - "supervisor_id": Supervisor User İD "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"


- Bütün işçilərə bax
    - endpoint: "http://localhost:8000/api/v1/users/?is_superuser=false&is_active=true"
    - Json-da gələn data:
        - "company": Şirkət
        - "department": Departament
        - "office": Ofis
        - "position": Vəzifə
        - "employee_status": İşçi statusu
        - "user_permissions": İcazə
        - "groups": İcazə Qrupu
        - "commission": Komissiya
        - "region": Şəhər, Bölgə
        - "is_superuser": Super Admindirmi
        - "username": Istifadəçi adı
        - "is_active": Aktivdirmi
        - "date_joined": Join tarixi
        - "fullname": Ad Soyad Ata adı
        - "phone_number_1": Telefon nömrəsi
        - "phone_number_2": Telefon nömrəsi
        - "address": Ünvan
        - "email": E-poçt
        - "photo_ID": Şəxsiyyət vəsiqəsi ön şəkli
        - "back_photo_of_ID": Şəxsiyyət vəsiqəsi arxa şəkli
        - "driving_license_photo": Sürücülük vəsiqəsi şəkli
        - "salary_style": Ə/H növü
        - "salary": Ə/H
        - "note": Qeyd
        - "electronic_signature": İmza
        - "profile_image": Profil şəkli
        - "contract_date": kontrakt tarixi
        - "register_type": Registrasiya növü
        - "supervisor": Supervizor

- Filter:
    - "http://localhost:8000/api/v1/users/?fullname=&fullname__icontains=&position__name=&position__name__icontains=&position=&is_superuser=unknown&salary_style=&register_type=&company=&company__name=&company__name__icontains=&office=&office__name=&office__name__icontains=&department=&department__name=&department__name__icontains=&is_active=unknown&employee_status=&employee_status__status_name=&employee_status__status_name__icontains=&contract_date=&contract_date__gte=&contract_date__lte="

- İD-ə görə işçi axtar
    - endpoint: "http://localhost:8000/api/v1/users/2/"

- İşçi sil
    - endpoint: "http://localhost:8000/api/v1/users/1/"
    - User-i deaktiv etmək üçün bu endpoint-ə delete sorğusu göndərilir. Delete sorğusu datanı database-dən silmir. Sadəcə is_active fieldini False edir.


Tarixçə
-------

- Tarixçəyə bax
    - endpoint: "http://localhost:8000/api/v1/salaries/employee-activity/?salary_view__employee__id=1"
    - Json-da gələn data:
        - "salary_view": Ə/H cədvəli.
            - "employee": İşçi
                - "company": sabit ə/h
                - "office": sabit ə/h
                - "position": sabit ə/h
                - "fullname": Ad soyad ata adı
                - "salary": sabit ə/h
            - "sale_quantity": Satış sayı
            - "commission_amount": Komissiya
            - "final_salary": Yekun
            - "date": Ə/h cədvəlinin aid olduğu tarix
        - "extra_data":
            - "total_working_day": İş Günü
            - "total_demo_count": Demo sayı
        - "bonus": Bonus
        - "advance_payment": Avans
        - "salary_deduction": Kəsinti
        - "salary_punishment": Cərimə
        - "activity_date": Tarixçənin aid olduğu tarix. Ə/h cədvəlinin date fieldi ilə eyni tarixi göstərir.

- Filter
    - endpoint: "http://localhost:8000/api/v1/salaries/employee-activity/?salary_view__employee__id=1&salary_view__final_salary=&salary_view__sale_quantity=&bonus=&advance_payment=&salary_deduction=&salary_punishment=&start_date=&end_date="
    - filterdəki start_date və end_date activity_date fieldinə görə hərəkət edir.