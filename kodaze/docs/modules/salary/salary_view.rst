#############################
SalaryView (Maaş Görüntüləmə)
#############################

- "employee"
    - (işçi - User)
- "sale_quantity"
    - (satış sayı - int)
- "sales_amount"
    - (ümumi satış məbləği - Float)
- "final_salary"
    - (yekun - Float)
- "date"
    - (tarix - Date)
- "is_done"
    - (status - Boolean)
- "advancepayment"
    - (avans - Float)
- "bonus"
    - (bonus - Float)
- "salarydeduction"
    - (kəsinti - Float)
- "salarypunishment"
    - (cərimə - Float)
- "total_advancepayment"
    - (ümumi avans - Float)
- "total_bonus"
    - (ümumi bonus - Float)
- "total_salarydeduction"
    - (ümumi kəsinti - Float)
- "total_salarypunishment"
    - (ümumi cərimə - Float)

=====

+-------------------+
|Get All SalaryView |
+-------------------+

Get All SalaryView
------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-views/"


+---------------------+
|Get SalaryView By ID |
+---------------------+

Get SalaryView By ID
--------------------

- endpoint: "http://localhost:8000/api/v1/salaries/salary-views/1/"