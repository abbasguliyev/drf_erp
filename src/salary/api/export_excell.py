import pandas as pd
from django.core.files import File
from salary.models import SalaryViewExport

def export_salary_view(data):
    excel_list = list()
    no = 0
    for d in data:
        excel_data = dict()
        no+=1
        try:
            fullname = d.get('employee').get('fullname')
        except:
            fullname = "-"
        try:
            company = d.get('employee').get('company').get('name')
        except:
            company = "-"
        try:
            office = d.get('employee').get('office').get('name')
        except:
            office = "-"
        try:
            position = d.get('employee').get('position').get('name')
        except:
            position = "-"
        work_day_count = d.get('extra_data').get('total_working_day')
        salary = d.get('employee').get('salary')
        sale_count = d.get('sale_quantity')
        commission = d.get('commission_amount')
        total_bonus = d.get('extra_data').get('total_bonus')
        total_advancepayment = d.get('extra_data').get('total_advancepayment')
        total_salarydeduction = d.get('extra_data').get('total_salarydeduction')
        total_salarypunishment = d.get('extra_data').get('total_salarypunishment')
        final_salary = d.get('final_salary')
        pay_date_qs = d.get('pay_date')
        if pay_date_qs is not None:
            pay_date = pay_date_qs
        else:
            pay_date = "-"

        is_done = d.get('is_done')
        if is_done is not False:
            status = "Ödənilib"
        else:
            status = "Ödənilməyib"

        excel_data['No'] = no
        excel_data['Ad Soyad'] = fullname
        excel_data['Şirkət'] = company
        excel_data['Ofis'] = office
        excel_data['Vəzifə'] = position
        excel_data['İş günü'] = work_day_count
        excel_data['Sabit'] = salary
        excel_data['Satış sayı'] = sale_count
        excel_data['Komissiya'] = commission
        excel_data['Bonus'] = total_bonus
        excel_data['Avans'] = total_advancepayment
        excel_data['Kəsinti'] = total_salarydeduction
        excel_data['Cərimə'] = total_salarypunishment
        excel_data['Yekun'] = final_salary
        excel_data['Ə/H ödəmə tarixi'] = pay_date
        excel_data['Status'] = status
        excel_list.append(excel_data)

    df = pd.DataFrame(excel_list)
    writer = pd.ExcelWriter("media/salary/salary-view-export.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1
    })

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    with open('media/salary/salary-view-export.xlsx', 'rb') as excel:
        last_obj = SalaryViewExport.objects.filter().last()
        if last_obj is not None:
            index = last_obj.id
        else:
            index = 1
        obj = SalaryViewExport()
        obj.file_data.save(f'salary-view-{index}.xlsx', File(excel))
    return obj.file_data
