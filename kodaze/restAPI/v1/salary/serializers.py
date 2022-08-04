from django.forms import ValidationError
from rest_framework import serializers
from account.models import IsciStatus, User
from company.models import Vezifeler
from restAPI.v1.company.serializers import VezifelerSerializer

from salary.models import (
    Avans,
    DealerPrimNew,
    Kesinti,
    Bonus,
    MaasGoruntuleme,
    MaasOde, 
    VanLeaderPrim, 
    DealerPrim, 
    OfficeLeaderPrim,
    CanvasserPrim,
    KreditorPrim,
    VanLeaderPrimNew
)

from restAPI.v1.account.serializers import IsciStatusSerializer, UserSerializer

class AvansSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True, many=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', many=True, write_only=True
    )

    class Meta:
        model = Avans
        fields = "__all__"

class KesintiSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True
    )

    class Meta:
        model = Kesinti
        fields = "__all__"
        
        
class BonusSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True
    )
  
    class Meta:
        model = Bonus
        fields = "__all__"

class MaasOdeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaasOde
        fields = ('isci', 'mebleg', 'qeyd', 'odeme_tarixi')
        read_only_fields = ('mebleg',)

class OfficeLeaderPrimSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = OfficeLeaderPrim
        fields = "__all__"
    
    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        vezife = validated_data.get('vezife')
        print(f"{prim_status=}")
        try:
            prim = OfficeLeaderPrim.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                raise ValidationError
            return super(OfficeLeaderPrimSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class VanLeaderPrimSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = VanLeaderPrim
        fields = "__all__"

class VanLeaderPrimNewSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = VanLeaderPrimNew
        fields = "__all__"

    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        vezife = validated_data.get('vezife')
        print(f"{prim_status=}")
        try:
            prim = VanLeaderPrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                raise ValidationError
            return super(VanLeaderPrimNewSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class DealerPrimSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = DealerPrim
        fields = "__all__"

class DealerPrimNewSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = DealerPrimNew
        fields = "__all__"

    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        vezife = validated_data.get('vezife')
        print(f"{prim_status=}")
        try:
            prim = DealerPrimNew.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                raise ValidationError
            return super(DealerPrimNewSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class CanvasserPrimSerializer(serializers.ModelSerializer):
    prim_status = IsciStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source="prim_status", write_only=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source="vezife", write_only=True
    )

    class Meta:
        model = CanvasserPrim
        fields = "__all__"
    
    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        vezife = validated_data.get('vezife')
        print(f"{prim_status=}")
        try:
            prim = CanvasserPrim.objects.filter(prim_status=prim_status, vezife=vezife)
            print(f"{prim=}")
            if len(prim)>0:
                raise ValidationError
            return super(CanvasserPrimSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class KreditorPrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = KreditorPrim
        fields = "__all__"

class MaasGoruntulemeSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        month = instance.tarix.month

        avans = Avans.objects.filter(isci = instance.isci, avans_tarixi__month=month)
        bonus = Bonus.objects.filter(isci = instance.isci, bonus_tarixi__month=month)
        kesinti = Kesinti.objects.filter(isci = instance.isci, kesinti_tarixi__month=month)

        umumi_avans = 0
        umumi_bonus = 0
        umumi_kesinti = 0

        for a in avans:
            umumi_avans += a.mebleg

        for b in bonus:
            umumi_bonus += b.mebleg

        for k in kesinti:
            umumi_kesinti += k.mebleg

        representation['avans'] = umumi_avans
        representation['bonus'] = umumi_bonus
        representation['kesinti'] = umumi_kesinti

        return representation
    
    class Meta:
        model = MaasGoruntuleme
        fields = '__all__'
        read_only_fields = ('avans', 'bonus', 'kesinti')