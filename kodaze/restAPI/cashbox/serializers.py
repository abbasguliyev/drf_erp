from rest_framework import serializers
from account.models import (
    User
)
from company.models import (
    Holding,
    Shirket,
    Ofis
)
from cashbox.models import (
    HoldingKassa,
    ShirketKassa,
    OfisKassa,
    PulAxini
)
from restAPI.company.serializers import HoldingSerializer, OfisSerializer, ShirketSerializer

class HoldingKassaSerializer(serializers.ModelSerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True
    )

    class Meta:
        model = HoldingKassa
        fields = "__all__"


class ShirketKassaSerializer(serializers.ModelSerializer):
    shirket = ShirketSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True
    )

    class Meta:
        model = ShirketKassa
        fields = "__all__"


class OfisKassaSerializer(serializers.ModelSerializer):
    ofis = OfisSerializer(read_only=True)
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True
    )

    class Meta:
        model = OfisKassa
        fields = "__all__"


class PulAxiniSerializer(serializers.ModelSerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True, required=False, allow_null=True
    )

    shirket = ShirketSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True, required=False, allow_null=True
    )

    ofis = OfisSerializer(read_only=True)
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True, required=False, allow_null=True
    )

    emeliyyat_eden = serializers.StringRelatedField()
    emeliyyat_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='emeliyyat_eden', write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = PulAxini
        fields = '__all__'
