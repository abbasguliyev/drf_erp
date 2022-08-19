import datetime
from rest_framework import serializers
from restAPI.v1.company.serializers import OfisSerializer, ShirketSerializer, ShobeSerializer

from restAPI.v1.account.serializers import MusteriSerializer, UserSerializer
from restAPI.v1.product.serializers import MehsullarSerializer

from contract.models import (
    MuqavileHediyye, 
    MuqavileKreditor,
    Muqavile, 
    OdemeTarix,  
    Deyisim, 
    DemoSatis
)

from services.models import (
    Servis,
)

from product.models import (
    Mehsullar,
)

from account.models import (
    User, 
    Musteri,
)

from company.models import (
    Shirket,
    Ofis,
    Shobe,
)
        
class ServisMuqavileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servis
        fields = ['id', 'yerine_yetirildi']

class MuqavileSerializer(serializers.ModelSerializer):
    vanleader = UserSerializer(read_only=True)
    dealer = UserSerializer(read_only=True)
    canvesser = UserSerializer(read_only=True)
    musteri = MusteriSerializer(read_only=True)
    mehsul = MehsullarSerializer(read_only=True)
    shirket = ShirketSerializer(read_only=True)
    shobe = ShobeSerializer(read_only=True)
    ofis = OfisSerializer(read_only=True)
    dusme_tarixi = serializers.DateField(read_only=True)
    is_sokuntu = serializers.BooleanField(read_only=True)
    borc_baglandi = serializers.BooleanField(read_only=True)

    servis_muqavile = ServisMuqavileSerializer(read_only=True, many=True)

    vanleader_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='vanleader', write_only=True, required=False, allow_null=True
    )
    dealer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='dealer', write_only=True, required=False, allow_null=True
    )
    canvesser_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='canvesser', write_only=True, required=False, allow_null=True
    )
    musteri_id = serializers.PrimaryKeyRelatedField(
        queryset=Musteri.objects.all(), source='musteri', write_only=True, required=False, allow_null=True
    )
    mehsul_id = serializers.PrimaryKeyRelatedField(
        queryset=Mehsullar.objects.all(), source='mehsul', write_only=True, required=False, allow_null=True
    )
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True, required=False, allow_null=True
    )

    shobe_id = serializers.PrimaryKeyRelatedField(
        queryset=Shobe.objects.all(), source='shobe', write_only=True, required=False, allow_null=True
    )

    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True, required=False, allow_null=True
    )

    muqavile_imzalanma_tarixi = serializers.DateField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        muqavile_kreditor = MuqavileKreditor.objects.filter(muqavile=instance).first()
        kreditor = None
        if muqavile_kreditor is not None:
            kreditor = dict()
            user_kreditor = muqavile_kreditor.kreditor
            muqavile_kreditor_id = muqavile_kreditor.id
            kreditor_asa = user_kreditor.asa

            kreditor['id'] = muqavile_kreditor_id
            kreditor['kreditor_asa'] = kreditor_asa
        
        representation['muqavile_kreditor'] = kreditor
        return representation

    def create(self, validated_data):
        muqavile_tarixi = validated_data.get('muqavile_tarixi')
        ilkin_odenis_tarixi = validated_data.get('ilkin_odenis_tarixi')
        odenis_uslubu = validated_data.get('odenis_uslubu')
        ilkin_odenis = validated_data.get('ilkin_odenis')
        if muqavile_tarixi == None:
            validated_data['muqavile_tarixi'] = datetime.date.today()
        if odenis_uslubu == "KREDİT":
            if float(ilkin_odenis) > 0:
                if ilkin_odenis_tarixi == None:
                    validated_data['ilkin_odenis_tarixi'] = datetime.date.today()
        return super(MuqavileSerializer, self).create(validated_data)

    class Meta:
        model = Muqavile
        fields = "__all__"
        read_only_fields = (
            'muqavile_umumi_mebleg', 
            'negd_odenis_gecikdirme', 
            'negd_odenis_1_status', 
            'negd_odenis_2_status',
            'ilkin_odenis_status',
            'qaliq_ilkin_odenis_status',
            'servis_muqavile',
            'qaliq_borc',
            'pdf_elave',
            'dusme_tarixi',
            'muqavile_imzalanma_tarixi',
            'is_sokuntu',
            'borc_baglandi'
        )

class MuqavileHediyyeSerializer(serializers.ModelSerializer):
    mehsul = MehsullarSerializer(read_only=True, many=True)
    muqavile = MuqavileSerializer(read_only=True)

    mehsul_id = serializers.PrimaryKeyRelatedField(
        queryset=Mehsullar.objects.all(), source='mehsul',  many=True, write_only=True
    )

    muqavile_id = serializers.PrimaryKeyRelatedField(
        queryset=Muqavile.objects.all(), source='muqavile', write_only=True
    )

    ofis = OfisSerializer(read_only=True)
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True, required=False, allow_null=True
    )

    hediyye_tarixi = serializers.DateField(read_only=True)


    class Meta:
        model = MuqavileHediyye
        fields = "__all__"
        read_only_fields = ('hediyye_tarixi',)


class OdemeTarixSerializer(serializers.ModelSerializer):
    muqavile = MuqavileSerializer(read_only=True)
    muqavile_id = serializers.PrimaryKeyRelatedField(
        queryset=Muqavile.objects.all(), source='muqavile', write_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        qalan_ay_sayi = 0
        odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=instance.muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status="BURAXILMIŞ AY")
        qalan_ay_sayi = len(odenmeyen_odemetarixler)
        representation['qalan_ay_sayi'] = qalan_ay_sayi

        return representation

    class Meta:
        model = OdemeTarix
        fields = "__all__"
        read_only_fields = ('sonuncu_ay', 'ay_no')

class DeyisimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deyisim
        fields = "__all__"

class DemoSatisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False, allow_null=True
    )
    sale_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = DemoSatis
        fields = "__all__"
        read_only_fields = ('sale_count',)


class MuqavileKreditorSerializer(serializers.ModelSerializer):
    muqavile = serializers.StringRelatedField(read_only=True)
    muqavile_id = serializers.PrimaryKeyRelatedField(
        queryset=Muqavile.objects.all(), source='muqavile', write_only=True
    )
    kreditor = serializers.StringRelatedField()
    kreditor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='kreditor', write_only=True
    )
    class Meta:
        model = MuqavileKreditor
        fields = '__all__'