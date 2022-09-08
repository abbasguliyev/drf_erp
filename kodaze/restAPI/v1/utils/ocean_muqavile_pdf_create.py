import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image
from contract.models import OdemeTarix

from reportlab.lib.utils import ImageReader

from core.settings import BASE_DIR, __PRODUCTION__
module_dir = os.path.dirname(__file__)  # get current directory



# ----------------------------------------------Muqavile pdf creater--------------------------------------------------------
def okean_muqavile_pdf_canvas(musteri, muqavile) -> list:
    """
    Bu metod muqavile pdf-ni lazimi melumatlarla doldurmaq isine baxir
    Args:
        muqavile:
        musteri:

    Returns: list which contains pdfs
    """

    asa = musteri.asa
    asa_split = asa.split(" ")

    if musteri.tel1 is not None:
        tel1 = musteri.tel1
    else:
        tel1 = ""
    if musteri.tel2 is not None:
        tel2 = musteri.tel2
    else:
        tel2 = ""

    if musteri.unvan is not None:
        unvan = musteri.unvan
    else:
        unvan = ""

    if musteri.bolge is not None:
        bolge = musteri.bolge.bolge_adi
    else:
        bolge = ""

    tarix_gun = muqavile.muqavile_tarixi.day
    tarix_month = muqavile.muqavile_tarixi.month
    tarix_year = muqavile.muqavile_tarixi.year
    mehsul_adi = muqavile.mehsul.mehsulun_adi
    
    if __PRODUCTION__== True:
        imza = os.path.join(BASE_DIR, f"{muqavile.elektron_imza}")
    else:
        imza = "/home/abbas/Workspace/kodazeERP/kodaze/media/media/imza.png"
    
    # imza = ImageReader(f"http://67.205.154.217:8000/media/media/{muqavile.elektron_imza}")

    # asa = "Abbas Quliyev Azər"
    # asa_split = asa.split(" ")
    # tel1 = "+994558327103"
    # tel2 = "+994558327103"
    # unvan = "Bakı şəhəri 20 yanvar dairəsi bina 25/4 mənzil 15 Bakı şəhəri 20 yanvar dairəsi bina 25/4 mənzil 15 Bakı şəhəri 20 yanvar dairəsi bina 25/4 mənzil 15"
    # bolge = "Bakı"

    # tarix_gun = "02"
    # tarix_month = "04"
    # tarix_year = "2022"
    # mehsul_adi = "Su filteri"
    # imza = "Abbas"

    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans','DejaVuSans.ttf'))
    i = 0
    while i < 3:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)
        if i == 0:
            can.drawString(55, 648, f"{bolge}")
            can.drawString(380, 647, f"{tarix_gun}")
            can.drawString(407, 647, f"{tarix_month} {tarix_year}")
            can.drawString(50, 537, f"{asa}")
            can.drawString(280, 410, f"{mehsul_adi}")
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            new_pdfs.append(new_pdf)
        if i == 1:
            can.drawString(155, 696, f"{mehsul_adi}")
            can.drawString(330, 634, f"{mehsul_adi}")
            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        if i == 2:
            can.drawString(352, 661, f"{mehsul_adi}")
            if len(asa_split) == 1:
                can.drawString(405, 482, f"{asa_split[0]}")
            elif len(asa_split) == 2:
                can.drawString(405, 482, f"{asa_split[0]} {asa_split[1]}")
            elif len(asa_split) == 3:
                can.drawString(405, 482, f"{asa_split[0]} {asa_split[1]}")
                can.drawString(340, 462, f"{asa_split[2]}")
            elif len(asa_split) == 4:
                can.drawString(405, 482, f"{asa_split[0]} {asa_split[1]}")
                can.drawString(340, 462, f"{asa_split[2]} {asa_split[3]}")

            can.drawString(373, 442, f"{tel1} {tel2}")
            can.drawString(410, 422, f"{unvan[:21]}")
            can.drawString(308, 404, f"{unvan[21:60]}")
            can.drawString(308, 388, f"{unvan[60:100]}")
            can.drawString(308, 374, f"{unvan[100:]}")
            # can.drawString(335, 270, f"{imza}")

            can.drawImage(x=335, y=270, image=imza, width=200, height=30)

            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def okean_create_muqavile_pdf(canvas,muqavile):
    """
    Bu method muqavile_pdf_canvas metodundan gelen pdf listin icindeki pdf-leri
    uygun olaraq bize verilen pdf-e merge edir.

    Args:
        canvas:

    Returns: final muqavile pdf which merged muqavile_pdf_canvas method's returns pdf

    """

    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(BASE_DIR, 'media/media/muqavile_doc/ocean-muqavile.pdf')
    file_path_new = os.path.join(f'media/media/muqavile_doc/ocean-muqavile-{muqavile.pk}.pdf')

    # ****** test **********
    # file_path = '/home/abbas/Workspace/alliance/OkeanCRM/media/media/muqavile_doc/ocean-muqavile.pdf'
    # file_path_new = os.path.join(f'/home/abbas/Workspace/alliance/OkeanCRM/media/media/muqavile-converted.pdf')
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

# muqavile_pdf_canvas = okean_muqavile_pdf_canvas(1,2)
# create_muqaivle_pdf = okean_create_muqaivle_pdf(muqavile_pdf_canvas, 1)


# ----------------------------------------------Kredit tarixleri pdf creater--------------------------------------------------------

def ocean_kredit_muqavile_pdf_canvas(muqavile) -> list:
    """
    Bu metod muqavile kredit pdf-ni lazimi melumatlarla doldurmaq isine baxir
    Args:
        muqavile:
        musteri:

    Returns: list which contains pdfs
    """

    tarix_gun = muqavile.muqavile_tarixi.day
    tarix_month = muqavile.muqavile_tarixi.month
    tarix_year = muqavile.muqavile_tarixi.year

    bolge = muqavile.musteri.bolge.bolge_adi
    musteri = muqavile.musteri

    odenis_uslubu = muqavile.odenis_uslubu

    asa = muqavile.musteri.asa
    asa_split = asa.split(" ")
    if musteri.tel1 is not None:
        tel1 = musteri.tel1
    else:
        tel1 = ""
    if musteri.tel2 is not None:
        tel2 = musteri.tel2
    else:
        tel2 = ""

    if musteri.unvan is not None:
        unvan = musteri.unvan
    else:
        unvan = ""

    mehsul_adi = muqavile.mehsul.mehsulun_adi
    mehsul_sayi = muqavile.mehsul_sayi

    if __PRODUCTION__==True:
        imza = os.path.join(BASE_DIR, f"{muqavile.elektron_imza}")
    else:
        imza = "/home/abbas/Workspace/kodazeERP/kodaze/media/media/imza.png"
  
    mehsul_qiymeti = muqavile.mehsul.qiymet * mehsul_sayi
    ilkin_odenis = muqavile.ilkin_odenis
    if ilkin_odenis == None or ilkin_odenis == "":
        ilkin_odenis = 0
    ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
    if ilkin_odenis_qaliq == None or ilkin_odenis_qaliq == "":
        ilkin_odenis_qaliq = 0
    ilkin_odenis_tam = float(ilkin_odenis) + float(ilkin_odenis_qaliq)
    if muqavile.ilkin_odenis_status == "BİTMİŞ":
        qalan_mebleg = float(mehsul_qiymeti) - float(ilkin_odenis)
    else:
        qalan_mebleg = float(mehsul_qiymeti) - float(ilkin_odenis_tam)

    odeme_tarixleri_list = []
    odeme_tarixleri = OdemeTarix.objects.filter(muqavile=muqavile)

    odeme_tarixleri_list = list(odeme_tarixleri)

    new_pdfs = []

    pdfmetrics.registerFont(TTFont('DejaVuSans','DejaVuSans.ttf'))

    i = 0
    while i < 4:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('DejaVuSans', 12)

        if i == 0:
            can.drawString(216, 736, f"{tarix_gun}")
            can.drawString(245, 736, f"{tarix_month}   {tarix_year}")

            can.drawString(80, 658, f"{bolge}")

            can.drawString(370, 658, f"{tarix_gun}")
            can.drawString(400, 658, f"{tarix_month}   {tarix_year}")

            can.drawString(270, 563, f"{asa}")

            can.drawString(65, 482, f"{mehsul_adi}")

            can.drawString(85, 422, f"{mehsul_qiymeti}")
            if odenis_uslubu == "KREDİT":
                can.drawString(200, 422, f"{ilkin_odenis}")
                can.drawString(305, 422, f"{ilkin_odenis_qaliq}")
                can.drawString(380, 422, f"{qalan_mebleg}")
            else:
                can.drawString(200, 422, "0")
                can.drawString(305, 422, "0")
                if odenis_uslubu == "NƏĞD":
                    can.drawString(380, 422, "0")
                

            if odenis_uslubu == "KREDİT":
                can.drawString(470, 422, f"{odenis_uslubu}")
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

            if odenis_uslubu == "KREDİT":
                try:
                    can.drawString(x1, 370, f"{odeme_tarixleri_list[0].tarix.day}")
                    can.drawString(x2, 370, f"{odeme_tarixleri_list[0].tarix.month}")
                    can.drawString(x3, 370, f"{odeme_tarixleri_list[0].tarix.year}")
                    can.drawString(x4, 365, f"{odeme_tarixleri_list[0].qiymet}")
                except:
                    can.drawString(x1, 370, f"")
                    can.drawString(x2, 370, f"")
                    can.drawString(x3, 370, f"")
                    can.drawString(x4, 365, f"")
                
                try:
                    can.drawString(x1, 345, f"{odeme_tarixleri_list[1].tarix.day}")
                    can.drawString(x2, 345, f"{odeme_tarixleri_list[1].tarix.month}")
                    can.drawString(x3, 345, f"{odeme_tarixleri_list[1].tarix.year}")
                    can.drawString(x4, 338, f"{odeme_tarixleri_list[1].qiymet}")
                except:
                    can.drawString(x1, 345, f"")
                    can.drawString(x2, 345, f"")
                    can.drawString(x3, 345, f"")
                    can.drawString(x4, 338, f"")
                try:
                    can.drawString(x1, 323, f"{odeme_tarixleri_list[2].tarix.day}")
                    can.drawString(x2, 323, f"{odeme_tarixleri_list[2].tarix.month}")
                    can.drawString(x3, 323, f"{odeme_tarixleri_list[2].tarix.year}")
                    can.drawString(x4, 316, f"{odeme_tarixleri_list[2].qiymet}")
                except:
                    can.drawString(x1, 323, f"")
                    can.drawString(x2, 323, f"")
                    can.drawString(x3, 323, f"")
                    can.drawString(x4, 316, f"")
                try:
                    can.drawString(x1, 298, f"{odeme_tarixleri_list[3].tarix.day}")
                    can.drawString(x2, 298, f"{odeme_tarixleri_list[3].tarix.month}")
                    can.drawString(x3, 298, f"{odeme_tarixleri_list[3].tarix.year}")
                    can.drawString(x4, 293, f"{odeme_tarixleri_list[3].qiymet}")
                except:
                    can.drawString(x1, 298, f"")
                    can.drawString(x2, 298, f"")
                    can.drawString(x3, 298, f"")
                    can.drawString(x4, 293, f"")
                try:
                    can.drawString(x1, 273, f"{odeme_tarixleri_list[4].tarix.day}")
                    can.drawString(x2, 273, f"{odeme_tarixleri_list[4].tarix.month}")
                    can.drawString(x3, 273, f"{odeme_tarixleri_list[4].tarix.year}")
                    can.drawString(x4, 265, f"{odeme_tarixleri_list[4].qiymet}")
                except:
                    can.drawString(x1, 273, f"")
                    can.drawString(x2, 273, f"")
                    can.drawString(x3, 273, f"")
                    can.drawString(x4, 265, f"")
                try:
                    can.drawString(x1, 250, f"{odeme_tarixleri_list[5].tarix.day}")
                    can.drawString(x2, 250, f"{odeme_tarixleri_list[5].tarix.month}")
                    can.drawString(x3, 250, f"{odeme_tarixleri_list[5].tarix.year}")
                    can.drawString(x4, 240, f"{odeme_tarixleri_list[5].qiymet}")
                except:
                    can.drawString(x1, 250, f"")
                    can.drawString(x2, 250, f"")
                    can.drawString(x3, 250, f"")
                    can.drawString(x4, 240, f"")
                try:
                    can.drawString(x1, 227, f"{odeme_tarixleri_list[6].tarix.day}")
                    can.drawString(x2, 227, f"{odeme_tarixleri_list[6].tarix.month}")
                    can.drawString(x3, 227, f"{odeme_tarixleri_list[6].tarix.year}")
                    can.drawString(x4, 218, f"{odeme_tarixleri_list[6].qiymet}")
                except:
                    can.drawString(x1, 227, f"")
                    can.drawString(x2, 227, f"")
                    can.drawString(x3, 227, f"")
                    can.drawString(x4, 218, f"")
                try:
                    can.drawString(x1, 203, f"{odeme_tarixleri_list[7].tarix.day}")
                    can.drawString(x2, 203, f"{odeme_tarixleri_list[7].tarix.month}")
                    can.drawString(x3, 203, f"{odeme_tarixleri_list[7].tarix.year}")
                    can.drawString(x4, 195, f"{odeme_tarixleri_list[7].qiymet}")
                except:
                    can.drawString(x1, 203, f"")
                    can.drawString(x2, 203, f"")
                    can.drawString(x3, 203, f"")
                    can.drawString(x4, 195, f"")
                try:
                    can.drawString(x1, 179, f"{odeme_tarixleri_list[8].tarix.day}")
                    can.drawString(x2, 179, f"{odeme_tarixleri_list[8].tarix.month}")
                    can.drawString(x3, 179, f"{odeme_tarixleri_list[8].tarix.year}")
                    can.drawString(x4, 172, f"{odeme_tarixleri_list[8].qiymet}")
                except:
                    can.drawString(x1, 179, f"")
                    can.drawString(x2, 179, f"")
                    can.drawString(x3, 179, f"")
                    can.drawString(x4, 172, f"")
                try:
                    can.drawString(x1, 154, f"{odeme_tarixleri_list[9].tarix.day}")
                    can.drawString(x2, 154, f"{odeme_tarixleri_list[9].tarix.month}")
                    can.drawString(x3, 154, f"{odeme_tarixleri_list[9].tarix.year}")
                    can.drawString(x4, 148, f"{odeme_tarixleri_list[9].qiymet}")
                except:
                    can.drawString(x1, 154, f"")
                    can.drawString(x2, 154, f"")
                    can.drawString(x3, 154, f"")
                    can.drawString(x4, 148, f"")
                try:
                    can.drawString(x1, 130, f"{odeme_tarixleri_list[10].tarix.day}")
                    can.drawString(x2, 130, f"{odeme_tarixleri_list[10].tarix.month}")
                    can.drawString(x3, 130, f"{odeme_tarixleri_list[10].tarix.year}")
                    can.drawString(x4, 122, f"{odeme_tarixleri_list[10].qiymet}")
                except:
                    can.drawString(x1, 130, f"")
                    can.drawString(x2, 130, f"")
                    can.drawString(x3, 130, f"")
                    can.drawString(x4, 122, f"")
                try:
                    can.drawString(x1, 106, f"{odeme_tarixleri_list[11].tarix.day}")
                    can.drawString(x2, 106, f"{odeme_tarixleri_list[11].tarix.month}")
                    can.drawString(x3, 106, f"{odeme_tarixleri_list[11].tarix.year}")
                    can.drawString(x4, 98, f"{odeme_tarixleri_list[11].qiymet}")
                except:
                    can.drawString(x1, 106, f"")
                    can.drawString(x2, 106, f"")
                    can.drawString(x3, 106, f"")
                    can.drawString(x4, 98, f"")
                
                try:
                    can.drawString(zx1, 370, f"{odeme_tarixleri_list[12].tarix.day}")
                    can.drawString(zx2, 370, f"{odeme_tarixleri_list[12].tarix.month}")
                    can.drawString(zx3, 370, f"{odeme_tarixleri_list[12].tarix.year}")
                    can.drawString(zx4, 365, f"{odeme_tarixleri_list[12].qiymet}")
                except:
                    can.drawString(zx1, 370, f"")
                    can.drawString(zx2, 370, f"")
                    can.drawString(zx3, 370, f"")
                    can.drawString(zx4, 365, f"")
                
                try:
                    can.drawString(zx1, 345, f"{odeme_tarixleri_list[13].tarix.day}")
                    can.drawString(zx2, 345, f"{odeme_tarixleri_list[13].tarix.month}")
                    can.drawString(zx3, 345, f"{odeme_tarixleri_list[13].tarix.year}")
                    can.drawString(zx4, 338, f"{odeme_tarixleri_list[13].qiymet}")
                except:
                    can.drawString(zx1, 345, f"")
                    can.drawString(zx2, 345, f"")
                    can.drawString(zx3, 345, f"")
                    can.drawString(zx4, 338, f"")
                try:
                    can.drawString(zx1, 323, f"{odeme_tarixleri_list[14].tarix.day}")
                    can.drawString(zx2, 323, f"{odeme_tarixleri_list[14].tarix.month}")
                    can.drawString(zx3, 323, f"{odeme_tarixleri_list[14].tarix.year}")
                    can.drawString(zx4, 316, f"{odeme_tarixleri_list[14].qiymet}")
                except:
                    can.drawString(zx1, 323, f"")
                    can.drawString(zx2, 323, f"")
                    can.drawString(zx3, 323, f"")
                    can.drawString(zx4, 316, f"")
                try:
                    can.drawString(zx1, 298, f"{odeme_tarixleri_list[15].tarix.day}")
                    can.drawString(zx2, 298, f"{odeme_tarixleri_list[15].tarix.month}")
                    can.drawString(zx3, 298, f"{odeme_tarixleri_list[15].tarix.year}")
                    can.drawString(zx4, 293, f"{odeme_tarixleri_list[15].qiymet}")
                except:
                    can.drawString(zx1, 298, f"")
                    can.drawString(zx2, 298, f"")
                    can.drawString(zx3, 298, f"")
                    can.drawString(zx4, 293, f"")
                try:
                    can.drawString(zx1, 273, f"{odeme_tarixleri_list[16].tarix.day}")
                    can.drawString(zx2, 273, f"{odeme_tarixleri_list[16].tarix.month}")
                    can.drawString(zx3, 273, f"{odeme_tarixleri_list[16].tarix.year}")
                    can.drawString(zx4, 265, f"{odeme_tarixleri_list[16].qiymet}")
                except:
                    can.drawString(zx1, 273, f"")
                    can.drawString(zx2, 273, f"")
                    can.drawString(zx3, 273, f"")
                    can.drawString(zx4, 265, f"")
                try:
                    can.drawString(zx1, 250, f"{odeme_tarixleri_list[17].tarix.day}")
                    can.drawString(zx2, 250, f"{odeme_tarixleri_list[17].tarix.month}")
                    can.drawString(zx3, 250, f"{odeme_tarixleri_list[17].tarix.year}")
                    can.drawString(zx4, 240, f"{odeme_tarixleri_list[17].qiymet}")
                except:
                    can.drawString(zx1, 250, f"")
                    can.drawString(zx2, 250, f"")
                    can.drawString(zx3, 250, f"")
                    can.drawString(zx4, 240, f"")
                try:
                    can.drawString(zx1, 227, f"{odeme_tarixleri_list[18].tarix.day}")
                    can.drawString(zx2, 227, f"{odeme_tarixleri_list[18].tarix.month}")
                    can.drawString(zx3, 227, f"{odeme_tarixleri_list[18].tarix.year}")
                    can.drawString(zx4, 218, f"{odeme_tarixleri_list[18].qiymet}")
                except:
                    can.drawString(zx1, 227, f"")
                    can.drawString(zx2, 227, f"")
                    can.drawString(zx3, 227, f"")
                    can.drawString(zx4, 218, f"")
                try:
                    can.drawString(zx1, 203, f"{odeme_tarixleri_list[19].tarix.day}")
                    can.drawString(zx2, 203, f"{odeme_tarixleri_list[19].tarix.month}")
                    can.drawString(zx3, 203, f"{odeme_tarixleri_list[19].tarix.year}")
                    can.drawString(zx4, 195, f"{odeme_tarixleri_list[19].qiymet}")
                except:
                    can.drawString(zx1, 203, f"")
                    can.drawString(zx2, 203, f"")
                    can.drawString(zx3, 203, f"")
                    can.drawString(zx4, 195, f"")
                try:
                    can.drawString(zx1, 179, f"{odeme_tarixleri_list[20].tarix.day}")
                    can.drawString(zx2, 179, f"{odeme_tarixleri_list[20].tarix.month}")
                    can.drawString(zx3, 179, f"{odeme_tarixleri_list[20].tarix.year}")
                    can.drawString(zx4, 172, f"{odeme_tarixleri_list[20].qiymet}")
                except:
                    can.drawString(zx1, 179, f"")
                    can.drawString(zx2, 179, f"")
                    can.drawString(zx3, 179, f"")
                    can.drawString(zx4, 172, f"")
                try:
                    can.drawString(zx1, 154, f"{odeme_tarixleri_list[21].tarix.day}")
                    can.drawString(zx2, 154, f"{odeme_tarixleri_list[21].tarix.month}")
                    can.drawString(zx3, 154, f"{odeme_tarixleri_list[21].tarix.year}")
                    can.drawString(zx4, 148, f"{odeme_tarixleri_list[21].qiymet}")
                except:
                    can.drawString(zx1, 154, f"")
                    can.drawString(zx2, 154, f"")
                    can.drawString(zx3, 154, f"")
                    can.drawString(zx4, 148, f"")
                try:
                    can.drawString(zx1, 130, f"{odeme_tarixleri_list[22].tarix.day}")
                    can.drawString(zx2, 130, f"{odeme_tarixleri_list[22].tarix.month}")
                    can.drawString(zx3, 130, f"{odeme_tarixleri_list[22].tarix.year}")
                    can.drawString(zx4, 122, f"{odeme_tarixleri_list[22].qiymet}")
                except:
                    can.drawString(zx1, 130, f"")
                    can.drawString(zx2, 130, f"")
                    can.drawString(zx3, 130, f"")
                    can.drawString(zx4, 122, f"")
                try:
                    can.drawString(zx1, 106, f"{odeme_tarixleri_list[23].tarix.day}")
                    can.drawString(zx2, 106, f"{odeme_tarixleri_list[23].tarix.month}")
                    can.drawString(zx3, 106, f"{odeme_tarixleri_list[23].tarix.year}")
                    can.drawString(zx4, 98, f"{odeme_tarixleri_list[23].qiymet}")
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
            can.drawString(73, 776, f"{mehsul_adi}")
            can.drawString(328, 776, f"{mehsul_sayi}")
            can.drawString(270, 556, f"{asa}")
            # can.drawString(500, 556, f"Imza")
            can.drawImage(x=400, y=555, image=imza, width=200, height=30)

            can.drawString(70, 462, f"{tarix_gun}")
            can.drawString(150, 462, f"{tarix_month}")
            can.drawString(210, 462, f"{tarix_year}")

            # can.drawString(352, 661, f"{mehsul_adi}")
            if len(asa_split) == 1:
                can.drawString(420, 295, f"{asa_split[0]}")
            elif len(asa_split) == 2:
                can.drawString(420, 295, f"{asa_split[0]} {asa_split[1]}")
            elif len(asa_split) == 3:
                can.drawString(420, 295, f"{asa_split[0]} {asa_split[1]}")
                can.drawString(340, 270, f"{asa_split[2]}")
            elif len(asa_split) == 4:
                can.drawString(420, 295, f"{asa_split[0]} {asa_split[1]}")
                can.drawString(340, 270, f"{asa_split[2]} {asa_split[3]}")

            can.drawString(361, 213, f"{unvan[:25]}")
            can.drawString(316, 185, f"{unvan[25:66]}")
            # can.drawString(361, 110, f"Imza")
            can.drawImage(x=361, y=110, image=imza, width=200, height=30)

            can.save()
            packet.seek(0)
            new_pdf1 = PdfFileReader(packet)
            new_pdfs.append(new_pdf1)
        i += 1

    return new_pdfs


def ocean_kredit_create_muqavile_pdf(canvas,muqavile):
    """
    Bu method ocean_kredit_muqavile_pdf_canvas metodundan gelen pdf listin icindeki pdf-leri
    uygun olaraq bize verilen pdf-e merge edir.

    Args:
        canvas:

    Returns: final muqavile pdf which merged muqavile_pdf_canvas method's returns pdf

    """

    new_pdfs = canvas
    # read your existing PDF
    file_path = os.path.join(BASE_DIR, 'media/media/muqavile_doc/ocean-muqavile-kredit.pdf')
    file_path_new = os.path.join(f'media/media/muqavile_doc/muqavile/ocean-muqavile-kredit-{muqavile.pk}.pdf')

    # ****** test **********
    # file_path = '/home/abbas/Workspace/alliance/OkeanCRM/media/media/muqavile_doc/ocean-muqavile-kredit.pdf'
    # file_path_new = os.path.join(f'/home/abbas/Workspace/alliance/OkeanCRM/media/media/ocean-muqavile-kredit1.pdf')
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