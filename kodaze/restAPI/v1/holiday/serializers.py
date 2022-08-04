from rest_framework import serializers
from account.models import User

from company.models import Holding, Komanda, Ofis, Shirket, Shobe, Vezifeler

from holiday.models import (
    HoldingGunler,
    IsciGelibGetmeVaxtlari,
    IsciGunler,
    KomandaGunler,
    KomandaIstisnaIsci,
    OfisGunler,
    OfisIstisnaIsci,
    ShirketGunler,
    ShirketIstisnaIsci,
    ShobeGunler,
    ShobeIstisnaIsci,
    VezifeGunler,
    HoldingIstisnaIsci,
    VezifeIstisnaIsci
)

from restAPI.v1.company.serializers import HoldingSerializer, KomandaSerializer, OfisSerializer, ShirketSerializer, ShobeSerializer, VezifelerSerializer
from restAPI.v1.account.serializers import UserSerializer


class HoldingGunlerSerializer(serializers.ModelSerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True
    )
    
    class Meta:
        model = HoldingGunler
        fields = "__all__"

class IsciGunlerSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True,
    )
    
    class Meta:
        model = IsciGunler
        fields = "__all__"

class IsciGelibGetmeVaxtlariSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True,
    )
    
    class Meta:
        model = IsciGelibGetmeVaxtlari
        fields = "__all__"


class KomandaGunlerSerializer(serializers.ModelSerializer):
    komanda = KomandaSerializer(read_only=True)
    komanda_id = serializers.PrimaryKeyRelatedField(
        queryset=Komanda.objects.all(), source='komanda', write_only=True,
    )
    
    class Meta:
        model = KomandaGunler
        fields = "__all__"

class OfisGunlerSerializer(serializers.ModelSerializer):
    ofis = OfisSerializer(read_only=True)
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True,
    )
    
    class Meta:
        model = OfisGunler
        fields = "__all__"

class ShirketGunlerSerializer(serializers.ModelSerializer):
    shirket = ShirketSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True
    )
    
    class Meta:
        model = ShirketGunler
        fields = "__all__"

class ShobeGunlerSerializer(serializers.ModelSerializer):
    shobe = ShobeSerializer(read_only=True)
    shobe_id = serializers.PrimaryKeyRelatedField(
        queryset=Shobe.objects.all(), source='shobe', write_only=True
    )
    
    class Meta:
        model = ShobeGunler
        fields = "__all__"

class VezifeGunlerSerializer(serializers.ModelSerializer):
    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source='vezife', write_only=True,
    )
    
    class Meta:
        model = VezifeGunler
        fields = "__all__"

# ------------------------------------------------------------------

class HoldingIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = HoldingGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = HoldingIstisnaIsci
        fields = "__all__"

class ShirketIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = ShirketGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = ShirketIstisnaIsci
        fields = "__all__"

class OfisIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = OfisGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=OfisGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = OfisIstisnaIsci
        fields = "__all__"

class ShobeIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = ShobeGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=ShobeGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = ShobeIstisnaIsci
        fields = "__all__"

class KomandaIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = KomandaGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=KomandaGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = KomandaIstisnaIsci
        fields = "__all__"

class VezifeIstisnaIsciSerializer(serializers.ModelSerializer):
    gunler = VezifeGunlerSerializer(read_only=True)
    gunler_id = serializers.PrimaryKeyRelatedField(
        queryset=VezifeGunler.objects.all(), source='gunler', write_only=True,
    )

    istisna_isciler = serializers.StringRelatedField(read_only=True, many=True)
    istisna_isciler_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='istisna_isciler', write_only=True, many=True
    )
    
    class Meta:
        model = VezifeIstisnaIsci
        fields = "__all__"