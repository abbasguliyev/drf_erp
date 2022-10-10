####################
CashFlow (Pul Axını)
####################

- holding
    - nullable. 
    - (Holding - Holdinq)
- company
    - nullable. 
    - (Company - Şirkət)
- office
    - nullable. 
    - (Office - Ofis)
- executor
    - nullable. 
    - (İşçi - User)
- date
    - (Tarix - Date)
- description
    - nullable. 
    - (Açıqlama - String)
- initial_balance
    - (İlkin balans - Float)
- subsequent_balance
    - (Sonrakı balans - Float)
- holding_initial_balance
    - (Holdinq İlkin balans - Float)
- holding_subsequent_balance
    - (Holdinq Sonrakı balans - Float)
- company_initial_balance
    - (Şirkət İlkin balans - Float)
- company_subsequent_balance
    - (Şirkət Sonrakı balans - Float)
- office_initial_balance
    - (Ofis İlkin balans - Float)
- office_subsequent_balance
    - (Ofis Sonrakı balans - Float)
- operation_style
    - (Əməliyyat növü - Enum<String>["MƏDAXİL", "MƏXARİC", "TRANSFER"])
- quantity
    - (miqdar - Float)


=====

+-----------------+
|Get All CashFlow |
+-----------------+

Get All CashFlow
----------------

- endpoint: "http://localhost:8000/api/v1/cashbox/cashflow/"


+-------------------+
|Get CashFlow By ID |
+-------------------+

Get CashFlow By ID
------------------

- endpoint: "http://localhost:8000/api/v1/cashbox/cashflow/1/"