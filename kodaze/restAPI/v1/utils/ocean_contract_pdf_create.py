import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image
from contract.models import Installment

from reportlab.lib.utils import ImageReader

from core.settings import BASE_DIR, __PRODUCTION__
module_dir = os.path.dirname(__file__)  # get current directory



# ----------------------------------------------Contract pdf creater--------------------------------------------------------
def ocean_contract_pdf_canvas(customer, contract) -> list:
    """
    Bu metod contract pdf-ni lazimi melumatlarla doldurmaq isine baxir
    Args:
        contract:
        customer:

    Returns: list which contains pdfs
    """

    fullname = customer.fullname
    fullname_split = fullname.split(" ")

    if customer.phone_number_1 is not None:
        phone_number_1 = customer.phone_number_1
    else:
        phone_number_1 = ""
    if customer.phone_number_2 is not None:
        phone_number_2 = customer.phone_number_2
    else:
        phone_number_2 = ""

    if customer.address is not None:
        address = customer.address
    else:
        address = ""

    if customer.region is not None:
        region = customer.region.region_name
    else:
        region = ""

    date_gun = contract.contract_date.day
    date_month = contract.contract_date.month
    date_year = contract.contract_date.year
    product_namei = contract.product.product_name
    
    if __PRODUCTION__== True:
        imza = os.path.join(BASE_DIR, f"{contract.electronic_signature}")
    else:
        imza = "/home/abbas/Workspace/kodazeERP/kodaze/media/media/imza.png"
    
    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans','DejaVuSans.ttf'))
    i = 0
    while i < 3:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)
        if i == 0:
            can.drawString(55, 648, f"{region}")
            can.drawString(380, 647, f"{date_gun}")
            can.drawString(407, 647, f"{date_month} {date_year}")
            can.drawString(50, 537, f"{fullname}")
            can.drawString(280, 410, f"{product_namei}")
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            new_pdfs.append(new_pdf)
        if i == 1:
            can.drawString(155, 696, f"{product_namei}")
            can.drawString(330, 634, f"{product_namei}")
            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        if i == 2:
            can.drawString(352, 661, f"{product_namei}")
            if len(fullname_split) == 1:
                can.drawString(405, 482, f"{fullname_split[0]}")
            elif len(fullname_split) == 2:
                can.drawString(405, 482, f"{fullname_split[0]} {fullname_split[1]}")
            elif len(fullname_split) == 3:
                can.drawString(405, 482, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 462, f"{fullname_split[2]}")
            elif len(fullname_split) == 4:
                can.drawString(405, 482, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 462, f"{fullname_split[2]} {fullname_split[3]}")

            can.drawString(373, 442, f"{phone_number_1} {phone_number_2}")
            can.drawString(410, 422, f"{address[:21]}")
            can.drawString(308, 404, f"{address[21:60]}")
            can.drawString(308, 388, f"{address[60:100]}")
            can.drawString(308, 374, f"{address[100:]}")
            # can.drawString(335, 270, f"{imza}")

            can.drawImage(x=335, y=270, image=imza, width=200, height=30)

            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def ocean_create_contract_pdf(canvas,contract):
    """
    Bu method contract_pdf_canvas metodundan gelen pdf listin icindeki pdf-leri
    uygun olaraq bize verilen pdf-e merge edir.

    Args:
        canvas:

    Returns: final contract pdf which merged contract_pdf_canvas method's returns pdf

    """

    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(BASE_DIR, 'media/media/contract_doc/ocean-contract.pdf')
    file_path_new = os.path.join(f'media/media/contract_doc/ocean-contract-{contract.pk}.pdf')

    # ****** test **********
    # file_path = '/home/abbas/Workspace/alliance/OkeanCRM/media/media/contract_doc/ocean-contract.pdf'
    # file_path_new = os.path.join(f'/home/abbas/Workspace/alliance/OkeanCRM/media/media/contract-converted.pdf')
    # **********************

    existing_pdf = PdfFileReader(
        open(file_path, "rb")
    )
    page_numbers = existing_pdf.pages.lengthFunction()
    output = PdfFileWriter()

    page1 = existing_pdf.getPage(0)
    page2 = existing_pdf.getPage(1)
    page3 = existing_pdf.getPage(2)
    page4 = existing_pdf.getPage(3)

    # 1-ci sehife
    page1.merge_page(new_pdfs[0].getPage(0))
    output.addPage(page1)

    outputStream1 = open(
        file_path_new,
        "wb")
    output.write(outputStream1)
    outputStream1.close()

    # 2-ci sehife
    output.addPage(page2)

    # 3-cu sehife
    page3.merge_page(new_pdfs[1].getPage(0))
    output.addPage(page3)
    # finally, write "output" to a real file
    outputStream2 = open(
        file_path_new,
        "wb")
    output.write(outputStream2)
    outputStream2.close()

    # 4-cu sehife
    page4.merge_page(new_pdfs[2].getPage(0))
    output.addPage(page4)

    # finally, write "output" to a real file
    outputStream3 = open(
        file_path_new,
        "wb")
    output.write(outputStream3)
    outputStream3.close()

    return file_path_new

# contract_pdf_canvas = okean_contract_pdf_canvas(1,2)
# create_muqaivle_pdf = okean_create_muqaivle_pdf(contract_pdf_canvas, 1)


# ----------------------------------------------Kredit dateleri pdf creater--------------------------------------------------------

def ocean_installment_contract_pdf_canvas(contract) -> list:
    """
    Bu metod contract installment pdf-ni lazimi melumatlarla doldurmaq isine baxir
    Args:
        contract:
        customer:

    Returns: list which contains pdfs
    """

    date_gun = contract.contract_date.day
    date_month = contract.contract_date.month
    date_year = contract.contract_date.year

    region = contract.customer.region.region_name
    customer = contract.customer

    payment_style = contract.payment_style

    fullname = contract.customer.fullname
    fullname_split = fullname.split(" ")
    if customer.phone_number_1 is not None:
        phone_number_1 = customer.phone_number_1
    else:
        phone_number_1 = ""
    if customer.phone_number_2 is not None:
        phone_number_2 = customer.phone_number_2
    else:
        phone_number_2 = ""

    if customer.address is not None:
        address = customer.address
    else:
        address = ""

    product_namei = contract.product.product_name
    product_quantity = contract.product_quantity

    if __PRODUCTION__==True:
        imza = os.path.join(BASE_DIR, f"{contract.electronic_signature}")
    else:
        imza = "/home/abbas/Workspace/kodazeERP/kodaze/media/media/imza.png"
  
    product_pricei = contract.product.price * product_quantity
    initial_payment = contract.initial_payment
    if initial_payment == None or initial_payment == "":
        initial_payment = 0
    initial_payment_debt = contract.initial_payment_debt
    if initial_payment_debt == None or initial_payment_debt == "":
        initial_payment_debt = 0
    initial_payment_tam = float(initial_payment) + float(initial_payment_debt)
    if contract.initial_payment_status == "BİTMİŞ":
        qalan_amount = float(product_pricei) - float(initial_payment)
    else:
        qalan_amount = float(product_pricei) - float(initial_payment_tam)

    payment_dateleri_list = []
    payment_dateleri = Installment.objects.filter(contract=contract)

    payment_dateleri_list = list(payment_dateleri)

    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans','DejaVuSans.ttf'))

    i = 0
    while i < 4:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)

        if i == 0:
            can.drawString(216, 736, f"{date_gun}")
            can.drawString(245, 736, f"{date_month}   {date_year}")

            can.drawString(80, 658, f"{region}")

            can.drawString(370, 658, f"{date_gun}")
            can.drawString(400, 658, f"{date_month}   {date_year}")

            can.drawString(270, 563, f"{fullname}")

            can.drawString(65, 482, f"{product_namei}")

            can.drawString(85, 422, f"{product_pricei}")
            if payment_style == "KREDİT":
                can.drawString(200, 422, f"{initial_payment}")
                can.drawString(305, 422, f"{initial_payment_debt}")
                can.drawString(380, 422, f"{qalan_amount}")
            else:
                can.drawString(200, 422, "0")
                can.drawString(305, 422, "0")
                if payment_style == "NƏĞD":
                    can.drawString(380, 422, "0")
                

            if payment_style == "KREDİT":
                can.drawString(470, 422, f"{payment_style}")
            else:
                can.drawString(470, 422, "NƏĞD")


            x1 = 95
            x2 = 126
            x3 = 150
            x4 = 220

            zx1 = 380
            zx2 = 411
            zx3 = 430
            zx4 = 495

            if payment_style == "KREDİT":
                try:
                    can.drawString(x1, 370, f"{payment_dateleri_list[0].date.day}")
                    can.drawString(x2, 370, f"{payment_dateleri_list[0].date.month}")
                    can.drawString(x3, 370, f"{payment_dateleri_list[0].date.year}")
                    can.drawString(x4, 365, f"{payment_dateleri_list[0].price}")
                except:
                    can.drawString(x1, 370, f"")
                    can.drawString(x2, 370, f"")
                    can.drawString(x3, 370, f"")
                    can.drawString(x4, 365, f"")
                
                try:
                    can.drawString(x1, 345, f"{payment_dateleri_list[1].date.day}")
                    can.drawString(x2, 345, f"{payment_dateleri_list[1].date.month}")
                    can.drawString(x3, 345, f"{payment_dateleri_list[1].date.year}")
                    can.drawString(x4, 338, f"{payment_dateleri_list[1].price}")
                except:
                    can.drawString(x1, 345, f"")
                    can.drawString(x2, 345, f"")
                    can.drawString(x3, 345, f"")
                    can.drawString(x4, 338, f"")
                try:
                    can.drawString(x1, 323, f"{payment_dateleri_list[2].date.day}")
                    can.drawString(x2, 323, f"{payment_dateleri_list[2].date.month}")
                    can.drawString(x3, 323, f"{payment_dateleri_list[2].date.year}")
                    can.drawString(x4, 316, f"{payment_dateleri_list[2].price}")
                except:
                    can.drawString(x1, 323, f"")
                    can.drawString(x2, 323, f"")
                    can.drawString(x3, 323, f"")
                    can.drawString(x4, 316, f"")
                try:
                    can.drawString(x1, 298, f"{payment_dateleri_list[3].date.day}")
                    can.drawString(x2, 298, f"{payment_dateleri_list[3].date.month}")
                    can.drawString(x3, 298, f"{payment_dateleri_list[3].date.year}")
                    can.drawString(x4, 293, f"{payment_dateleri_list[3].price}")
                except:
                    can.drawString(x1, 298, f"")
                    can.drawString(x2, 298, f"")
                    can.drawString(x3, 298, f"")
                    can.drawString(x4, 293, f"")
                try:
                    can.drawString(x1, 273, f"{payment_dateleri_list[4].date.day}")
                    can.drawString(x2, 273, f"{payment_dateleri_list[4].date.month}")
                    can.drawString(x3, 273, f"{payment_dateleri_list[4].date.year}")
                    can.drawString(x4, 265, f"{payment_dateleri_list[4].price}")
                except:
                    can.drawString(x1, 273, f"")
                    can.drawString(x2, 273, f"")
                    can.drawString(x3, 273, f"")
                    can.drawString(x4, 265, f"")
                try:
                    can.drawString(x1, 250, f"{payment_dateleri_list[5].date.day}")
                    can.drawString(x2, 250, f"{payment_dateleri_list[5].date.month}")
                    can.drawString(x3, 250, f"{payment_dateleri_list[5].date.year}")
                    can.drawString(x4, 240, f"{payment_dateleri_list[5].price}")
                except:
                    can.drawString(x1, 250, f"")
                    can.drawString(x2, 250, f"")
                    can.drawString(x3, 250, f"")
                    can.drawString(x4, 240, f"")
                try:
                    can.drawString(x1, 227, f"{payment_dateleri_list[6].date.day}")
                    can.drawString(x2, 227, f"{payment_dateleri_list[6].date.month}")
                    can.drawString(x3, 227, f"{payment_dateleri_list[6].date.year}")
                    can.drawString(x4, 218, f"{payment_dateleri_list[6].price}")
                except:
                    can.drawString(x1, 227, f"")
                    can.drawString(x2, 227, f"")
                    can.drawString(x3, 227, f"")
                    can.drawString(x4, 218, f"")
                try:
                    can.drawString(x1, 203, f"{payment_dateleri_list[7].date.day}")
                    can.drawString(x2, 203, f"{payment_dateleri_list[7].date.month}")
                    can.drawString(x3, 203, f"{payment_dateleri_list[7].date.year}")
                    can.drawString(x4, 195, f"{payment_dateleri_list[7].price}")
                except:
                    can.drawString(x1, 203, f"")
                    can.drawString(x2, 203, f"")
                    can.drawString(x3, 203, f"")
                    can.drawString(x4, 195, f"")
                try:
                    can.drawString(x1, 179, f"{payment_dateleri_list[8].date.day}")
                    can.drawString(x2, 179, f"{payment_dateleri_list[8].date.month}")
                    can.drawString(x3, 179, f"{payment_dateleri_list[8].date.year}")
                    can.drawString(x4, 172, f"{payment_dateleri_list[8].price}")
                except:
                    can.drawString(x1, 179, f"")
                    can.drawString(x2, 179, f"")
                    can.drawString(x3, 179, f"")
                    can.drawString(x4, 172, f"")
                try:
                    can.drawString(x1, 154, f"{payment_dateleri_list[9].date.day}")
                    can.drawString(x2, 154, f"{payment_dateleri_list[9].date.month}")
                    can.drawString(x3, 154, f"{payment_dateleri_list[9].date.year}")
                    can.drawString(x4, 148, f"{payment_dateleri_list[9].price}")
                except:
                    can.drawString(x1, 154, f"")
                    can.drawString(x2, 154, f"")
                    can.drawString(x3, 154, f"")
                    can.drawString(x4, 148, f"")
                try:
                    can.drawString(x1, 130, f"{payment_dateleri_list[10].date.day}")
                    can.drawString(x2, 130, f"{payment_dateleri_list[10].date.month}")
                    can.drawString(x3, 130, f"{payment_dateleri_list[10].date.year}")
                    can.drawString(x4, 122, f"{payment_dateleri_list[10].price}")
                except:
                    can.drawString(x1, 130, f"")
                    can.drawString(x2, 130, f"")
                    can.drawString(x3, 130, f"")
                    can.drawString(x4, 122, f"")
                try:
                    can.drawString(x1, 106, f"{payment_dateleri_list[11].date.day}")
                    can.drawString(x2, 106, f"{payment_dateleri_list[11].date.month}")
                    can.drawString(x3, 106, f"{payment_dateleri_list[11].date.year}")
                    can.drawString(x4, 98, f"{payment_dateleri_list[11].price}")
                except:
                    can.drawString(x1, 106, f"")
                    can.drawString(x2, 106, f"")
                    can.drawString(x3, 106, f"")
                    can.drawString(x4, 98, f"")
                
                try:
                    can.drawString(zx1, 370, f"{payment_dateleri_list[12].date.day}")
                    can.drawString(zx2, 370, f"{payment_dateleri_list[12].date.month}")
                    can.drawString(zx3, 370, f"{payment_dateleri_list[12].date.year}")
                    can.drawString(zx4, 365, f"{payment_dateleri_list[12].price}")
                except:
                    can.drawString(zx1, 370, f"")
                    can.drawString(zx2, 370, f"")
                    can.drawString(zx3, 370, f"")
                    can.drawString(zx4, 365, f"")
                
                try:
                    can.drawString(zx1, 345, f"{payment_dateleri_list[13].date.day}")
                    can.drawString(zx2, 345, f"{payment_dateleri_list[13].date.month}")
                    can.drawString(zx3, 345, f"{payment_dateleri_list[13].date.year}")
                    can.drawString(zx4, 338, f"{payment_dateleri_list[13].price}")
                except:
                    can.drawString(zx1, 345, f"")
                    can.drawString(zx2, 345, f"")
                    can.drawString(zx3, 345, f"")
                    can.drawString(zx4, 338, f"")
                try:
                    can.drawString(zx1, 323, f"{payment_dateleri_list[14].date.day}")
                    can.drawString(zx2, 323, f"{payment_dateleri_list[14].date.month}")
                    can.drawString(zx3, 323, f"{payment_dateleri_list[14].date.year}")
                    can.drawString(zx4, 316, f"{payment_dateleri_list[14].price}")
                except:
                    can.drawString(zx1, 323, f"")
                    can.drawString(zx2, 323, f"")
                    can.drawString(zx3, 323, f"")
                    can.drawString(zx4, 316, f"")
                try:
                    can.drawString(zx1, 298, f"{payment_dateleri_list[15].date.day}")
                    can.drawString(zx2, 298, f"{payment_dateleri_list[15].date.month}")
                    can.drawString(zx3, 298, f"{payment_dateleri_list[15].date.year}")
                    can.drawString(zx4, 293, f"{payment_dateleri_list[15].price}")
                except:
                    can.drawString(zx1, 298, f"")
                    can.drawString(zx2, 298, f"")
                    can.drawString(zx3, 298, f"")
                    can.drawString(zx4, 293, f"")
                try:
                    can.drawString(zx1, 273, f"{payment_dateleri_list[16].date.day}")
                    can.drawString(zx2, 273, f"{payment_dateleri_list[16].date.month}")
                    can.drawString(zx3, 273, f"{payment_dateleri_list[16].date.year}")
                    can.drawString(zx4, 265, f"{payment_dateleri_list[16].price}")
                except:
                    can.drawString(zx1, 273, f"")
                    can.drawString(zx2, 273, f"")
                    can.drawString(zx3, 273, f"")
                    can.drawString(zx4, 265, f"")
                try:
                    can.drawString(zx1, 250, f"{payment_dateleri_list[17].date.day}")
                    can.drawString(zx2, 250, f"{payment_dateleri_list[17].date.month}")
                    can.drawString(zx3, 250, f"{payment_dateleri_list[17].date.year}")
                    can.drawString(zx4, 240, f"{payment_dateleri_list[17].price}")
                except:
                    can.drawString(zx1, 250, f"")
                    can.drawString(zx2, 250, f"")
                    can.drawString(zx3, 250, f"")
                    can.drawString(zx4, 240, f"")
                try:
                    can.drawString(zx1, 227, f"{payment_dateleri_list[18].date.day}")
                    can.drawString(zx2, 227, f"{payment_dateleri_list[18].date.month}")
                    can.drawString(zx3, 227, f"{payment_dateleri_list[18].date.year}")
                    can.drawString(zx4, 218, f"{payment_dateleri_list[18].price}")
                except:
                    can.drawString(zx1, 227, f"")
                    can.drawString(zx2, 227, f"")
                    can.drawString(zx3, 227, f"")
                    can.drawString(zx4, 218, f"")
                try:
                    can.drawString(zx1, 203, f"{payment_dateleri_list[19].date.day}")
                    can.drawString(zx2, 203, f"{payment_dateleri_list[19].date.month}")
                    can.drawString(zx3, 203, f"{payment_dateleri_list[19].date.year}")
                    can.drawString(zx4, 195, f"{payment_dateleri_list[19].price}")
                except:
                    can.drawString(zx1, 203, f"")
                    can.drawString(zx2, 203, f"")
                    can.drawString(zx3, 203, f"")
                    can.drawString(zx4, 195, f"")
                try:
                    can.drawString(zx1, 179, f"{payment_dateleri_list[20].date.day}")
                    can.drawString(zx2, 179, f"{payment_dateleri_list[20].date.month}")
                    can.drawString(zx3, 179, f"{payment_dateleri_list[20].date.year}")
                    can.drawString(zx4, 172, f"{payment_dateleri_list[20].price}")
                except:
                    can.drawString(zx1, 179, f"")
                    can.drawString(zx2, 179, f"")
                    can.drawString(zx3, 179, f"")
                    can.drawString(zx4, 172, f"")
                try:
                    can.drawString(zx1, 154, f"{payment_dateleri_list[21].date.day}")
                    can.drawString(zx2, 154, f"{payment_dateleri_list[21].date.month}")
                    can.drawString(zx3, 154, f"{payment_dateleri_list[21].date.year}")
                    can.drawString(zx4, 148, f"{payment_dateleri_list[21].price}")
                except:
                    can.drawString(zx1, 154, f"")
                    can.drawString(zx2, 154, f"")
                    can.drawString(zx3, 154, f"")
                    can.drawString(zx4, 148, f"")
                try:
                    can.drawString(zx1, 130, f"{payment_dateleri_list[22].date.day}")
                    can.drawString(zx2, 130, f"{payment_dateleri_list[22].date.month}")
                    can.drawString(zx3, 130, f"{payment_dateleri_list[22].date.year}")
                    can.drawString(zx4, 122, f"{payment_dateleri_list[22].price}")
                except:
                    can.drawString(zx1, 130, f"")
                    can.drawString(zx2, 130, f"")
                    can.drawString(zx3, 130, f"")
                    can.drawString(zx4, 122, f"")
                try:
                    can.drawString(zx1, 106, f"{payment_dateleri_list[23].date.day}")
                    can.drawString(zx2, 106, f"{payment_dateleri_list[23].date.month}")
                    can.drawString(zx3, 106, f"{payment_dateleri_list[23].date.year}")
                    can.drawString(zx4, 98, f"{payment_dateleri_list[23].price}")
                except:
                    can.drawString(zx1, 106, f"")
                    can.drawString(zx2, 106, f"")
                    can.drawString(zx3, 106, f"")
                    can.drawString(zx4, 98, f"")
            
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            new_pdfs.append(new_pdf)
        if i == 1:
            can.drawString(73, 776, f"{product_namei}")
            can.drawString(328, 776, f"{product_quantity}")
            can.drawString(270, 556, f"{fullname}")
            # can.drawString(500, 556, f"Imza")
            can.drawImage(x=400, y=555, image=imza, width=200, height=30)

            can.drawString(70, 462, f"{date_gun}")
            can.drawString(150, 462, f"{date_month}")
            can.drawString(210, 462, f"{date_year}")

            # can.drawString(352, 661, f"{product_namei}")
            if len(fullname_split) == 1:
                can.drawString(420, 295, f"{fullname_split[0]}")
            elif len(fullname_split) == 2:
                can.drawString(420, 295, f"{fullname_split[0]} {fullname_split[1]}")
            elif len(fullname_split) == 3:
                can.drawString(420, 295, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 270, f"{fullname_split[2]}")
            elif len(fullname_split) == 4:
                can.drawString(420, 295, f"{fullname_split[0]} {fullname_split[1]}")
                can.drawString(340, 270, f"{fullname_split[2]} {fullname_split[3]}")

            can.drawString(361, 213, f"{address[:25]}")
            can.drawString(316, 185, f"{address[25:66]}")
            # can.drawString(361, 110, f"Imza")
            can.drawImage(x=361, y=110, image=imza, width=200, height=30)

            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def ocean_installment_create_contract_pdf(canvas,contract):
    """
    Bu method ocean_installment_contract_pdf_canvas metodundan gelen pdf listin icindeki pdf-leri
    uygun olaraq bize verilen pdf-e merge edir.

    Args:
        canvas:

    Returns: final contract pdf which merged contract_pdf_canvas method's returns pdf

    """

    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(BASE_DIR, 'media/media/contract_doc/ocean-contract-installment.pdf')
    file_path_new = os.path.join(f'media/media/contract_doc/ocean-contract-installment-{contract.pk}.pdf')

    # ****** test **********
    # file_path = '/home/abbas/Workspace/alliance/OkeanCRM/media/media/contract_doc/ocean-contract-installment.pdf'
    # file_path_new = os.path.join(f'/home/abbas/Workspace/alliance/OkeanCRM/media/media/ocean-contract-installment1.pdf')
    # **********************

    existing_pdf = PdfFileReader(
        open(file_path, "rb")
    )
    page_numbers = existing_pdf.pages.lengthFunction()
    output = PdfFileWriter()

    page1 = existing_pdf.getPage(0)
    page2 = existing_pdf.getPage(1)

    # 1-ci sehife
    page1.merge_page(new_pdfs[0].getPage(0))
    output.addPage(page1)

    outputStream1 = open(
        file_path_new,
        "wb")
    output.write(outputStream1)
    outputStream1.close()

    # 3-cu sehife
    page2.merge_page(new_pdfs[1].getPage(0))
    output.addPage(page2)
    # finally, write "output" to a real file
    outputStream2 = open(
        file_path_new,
        "wb")
    output.write(outputStream2)
    outputStream2.close()

    return file_path_new