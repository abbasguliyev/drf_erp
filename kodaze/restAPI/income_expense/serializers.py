from rest_framework import serializers

from account.models import (
    User
)

from income_expense.models import (
    HoldingKassaMedaxil,
    HoldingKassaMexaric,
    OfisKassaMedaxil,
    OfisKassaMexaric,
    ShirketKassaMedaxil,
    ShirketKassaMexaric
)

from cashbox.models import HoldingKassa, OfisKassa, ShirketKassa

from restAPI.cashbox.serializers import (
    HoldingKassaSerializer, 
    OfisKassaSerializer, 
    ShirketKassaSerializer
)

class HoldingKassaMedaxilSerializer(serializers.ModelSerializer):
    medaxil_eden = serializers.StringRelatedField()
    medaxil_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='medaxil_eden', write_only=True, required=False, allow_null=True
    )
    holding_kassa = HoldingKassaSerializer(read_only=True)
    holding_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingKassa.objects.all(), source='holding_kassa', write_only=True
    )

    class Meta:
        model = HoldingKassaMedaxil
        fields = "__all__"
        read_only_fields = ('evvelki_balans', 'sonraki_balans')


class HoldingKassaMexaricSerializer(serializers.ModelSerializer):
    mexaric_eden = serializers.StringRelatedField()
    mexaric_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='mexaric_eden', write_only=True, required=False, allow_null=True
    )
    holding_kassa = HoldingKassaSerializer(read_only=True)
    holding_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingKassa.objects.all(), source='holding_kassa', write_only=True
    )

    class Meta:
        model = HoldingKassaMexaric
        fields = "__all__"
        read_only_fields = ('evvelki_balans', 'sonraki_balans')


class ShirketKassaMedaxilSerializer(serializers.ModelSerializer):
    medaxil_eden = serializers.StringRelatedField()
    medaxil_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='medaxil_eden', write_only=True, required=False, allow_null=True
    )
    shirket_kassa = ShirketKassaSerializer(read_only=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', write_only=True
    )

    class Meta:
        model = ShirketKassaMedaxil
        fields = "__all__"
        read_only_fields = ('evvelki_balans', 'sonraki_balans')


class ShirketKassaMexaricSerializer(serializers.ModelSerializer):
    mexaric_eden = serializers.StringRelatedField()
    mexaric_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='mexaric_eden', write_only=True, required=False, allow_null=True
    )
    shirket_kassa = ShirketKassaSerializer(read_only=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', write_only=True
    )

    class Meta:
        model = ShirketKassaMexaric
        fields = "__all__"
        read_only_fields = ('evvelki_balans', 'sonraki_balans')


class OfisKassaMedaxilSerializer(serializers.ModelSerializer):
    medaxil_eden = serializers.StringRelatedField()
    medaxil_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='medaxil_eden', write_only=True, required=False, allow_null=True
    )
    ofis_kassa = OfisKassaSerializer(read_only=True)
    ofis_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=OfisKassa.objects.all(), source='ofis_kassa', write_only=True
    )

    class Meta:
        model = OfisKassaMedaxil
        fields = '__all__'
        read_only_fields = ('evvelki_balans', 'sonraki_balans')


class OfisKassaMexaricSerializer(serializers.ModelSerializer):
    mexaric_eden = serializers.StringRelatedField()
    mexaric_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='mexaric_eden', write_only=True, required=False, allow_null=True
    )
    ofis_kassa = OfisKassaSerializer(read_only=True)
    ofis_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=OfisKassa.objects.all(), source='ofis_kassa', write_only=True
    )

    class Meta:
        model = OfisKassaMexaric
        fields = '__all__'
        read_only_fields = ('evvelki_balans', 'sonraki_balans')