import datetime
from cashbox.models import HoldingKassa, OfisKassa, PulAxini, ShirketKassa

def holding_umumi_balans_hesabla():
    umumi_balans = 0

    holding_kassa = HoldingKassa.objects.all()
    holding_balans = 0
    for hk in holding_kassa:
        holding_balans += float(hk.balans)

    shirket_kassa = ShirketKassa.objects.all()
    shirket_balans = 0
    for sk in shirket_kassa:
        shirket_balans += float(sk.balans)

    ofis_kassa = OfisKassa.objects.all()
    ofis_balans = 0
    for ok in ofis_kassa:
        ofis_balans += float(ok.balans)

    umumi_balans = holding_balans + shirket_balans + ofis_balans
    return umumi_balans

def holding_balans_hesabla():
    holding_balans = 0
    holding_kassa = HoldingKassa.objects.all()[0]
    holding_balans += float(holding_kassa.balans)
    return holding_balans

def shirket_balans_hesabla(shirket):
    shirket_balans = 0
    shirket_kassa = ShirketKassa.objects.get(shirket=shirket)
    shirket_balans += float(shirket_kassa.balans)
    return shirket_balans

def ofis_balans_hesabla(ofis):
    ofis_balans = 0
    ofis_kassa = OfisKassa.objects.get(ofis=ofis)
    ofis_balans += float(ofis_kassa.balans)
    return ofis_balans

def pul_axini_create(
    holding=None, 
    shirket=None, 
    ofis=None, 
    tarix=datetime.date.today(), 
    emeliyyat_uslubu=None, 
    aciqlama=None, 
    ilkin_balans=0, 
    sonraki_balans=0, 
    miqdar=0, 
    emeliyyat_eden=None,
    holding_ilkin_balans=0,
    holding_sonraki_balans=0,
    shirket_ilkin_balans=0,
    shirket_sonraki_balans=0,
    ofis_ilkin_balans=0,
    ofis_sonraki_balans=0,
):
    """
    Pul axinlarini create eden funksiya
    """

    pul_axini = PulAxini.objects.create(
        holding=holding,
        shirket=shirket,
        ofis=ofis,
        tarix=tarix,
        emeliyyat_uslubu=emeliyyat_uslubu,
        aciqlama=aciqlama,
        ilkin_balans=ilkin_balans,
        sonraki_balans=sonraki_balans,
        emeliyyat_eden=emeliyyat_eden,
        holding_ilkin_balans=holding_ilkin_balans,
        holding_sonraki_balans=holding_sonraki_balans,
        shirket_ilkin_balans=shirket_ilkin_balans,
        shirket_sonraki_balans=shirket_sonraki_balans,
        ofis_ilkin_balans=ofis_ilkin_balans,
        ofis_sonraki_balans=ofis_sonraki_balans,
        miqdar=miqdar
    )
    return pul_axini.save()