###################
Product (Məhsullar)
###################

- "product_name"
    - required. 
    - Mutleq gonderilmelidir
    - (Məhsulun adı - String)
- "barcode"
    - nullable. 
    - (Məhsulun barkodu - Integer)
- "price"
    - required. 
    - Mutleq gonderilmelidir
    - (Məhsulun qiyməti - Float)
- "company_id"
    - required. 
    - Mutleq gonderilmelidir
    - (Şirkət İD - Company)
- "category_id"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Kateqoriya - Category)
- "unit_of_measure_id"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Ölçü vahidi - UnitOfMeasure)
- "volume"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Həcmi - Float)
- "weight"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Çəkisi - Float)
- "width"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Eni - Float)
- "length"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Uzunluğu - Float)
- "height"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Hündürlüyü - Float)
- "note"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Qeyd - String)
- "product_image"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Məhsulun şəkli - İmage)
- "is_gift"
    - nullable. 
    - Mutleq gonderilmelidir
    - (Hədiyyədirmi - Boolean)

=====

+---------------+
|Product create |
+---------------+

Product create
--------------

- endpoint: "http://localhost:8000/api/v1/product/"

.. code:: json

  {
    "company_id": "",
    "category_id": "",
    "unit_of_measure_id": "",
    "product_name": "",
    "barcode": "",
    "price": "",
    "volume": "",
    "weight": "",
    "width": "",
    "length": "",
    "height": "",
    "note": "",
    "product_image": "",
    "is_gift": false
  }

+---------------+
|Update Product |
+---------------+

Update Product
--------------

- endpoint: "http://localhost:8000/api/v1/product/1/"
- put sorğusu patch kimi işləyir. Fieldlər tək tək və ya toplu şəkildə update edilə bilinir

.. code:: json

  {
    "company_id": "",
    "category_id": "",
    "unit_of_measure_id": "",
    "product_name": "",
    "barcode": "",
    "price": "",
    "volume": "",
    "weight": "",
    "width": "",
    "length": "",
    "height": "",
    "note": "",
    "product_image": "",
    "is_gift": false
  }
  
+----------------+
|Get All Product |
+----------------+

Get All Product
---------------

- endpoint: "http://localhost:8000/api/v1/product/"


+------------------+
|Get Product By ID |
+------------------+

Get Product By ID
-----------------

- endpoint: "http://localhost:8000/api/v1/product/1/"

+---------------+
|Delete Product |
+---------------+

Delete Product
--------------

- endpoint: "http://localhost:8000/api/v1/product/1/"