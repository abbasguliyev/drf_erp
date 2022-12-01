#######
İşçilər
#######

+-------+
|İşçilər|
+-------+

İşçilər
-------

- İşçi register etmək
    - endpoint "http://localhost:8000/api/v1/users/register/"
    - İşçi register edərkən username user-{userID} şəklində avtomatik create olur. Update bölməsindən dəyişə bilinir.
    - İşçilər 2 formada register edilir. Holding işçiləri və Şirkət işçiləri. register_type fieldində Şirkət və ya Holding seçilərək edilir.
        Şirkət işçisi daxil ediliyi zaman mütləq 
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
        - "employee_status": nullable - EmployeeStatus İD - işçi statusu
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

