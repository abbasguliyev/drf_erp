from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import (
    User
)
from cashbox.models import HoldingKassa, OfisKassa, ShirketKassa
from restAPI.cashbox.serializers import HoldingKassaSerializer, OfisKassaSerializer, ShirketKassaSerializer

from transfer.models import (
    HoldingdenShirketlereTransfer,
    OfisdenShirketeTransfer,
    ShirketdenHoldingeTransfer,
    ShirketdenOfislereTransfer
)

from contract.models import Muqavile, MuqavileKreditor
from django.contrib.auth.models import Group


class HoldingdenShirketlereTransferSerializer(serializers.ModelSerializer):
    transfer_eden = serializers.StringRelatedField()
    transfer_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='transfer_eden', write_only=True, required=False, allow_null=True
    )
    holding_kassa = HoldingKassaSerializer(read_only=True)
    holding_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingKassa.objects.all(), source='holding_kassa', write_only=True
    )

    shirket_kassa = ShirketKassaSerializer(read_only=True, many=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', many=True, write_only=True
    )

    class Meta:
        model = HoldingdenShirketlereTransfer
        fields = "__all__"
        read_only_fields = ('qalan_mebleg', 'evvelki_balans', 'sonraki_balans')


class ShirketdenHoldingeTransferSerializer(serializers.ModelSerializer):
    transfer_eden = serializers.StringRelatedField()
    transfer_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='transfer_eden', write_only=True, required=False, allow_null=True
    )
    shirket_kassa = ShirketKassaSerializer(read_only=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', write_only=True
    )

    holding_kassa = HoldingKassaSerializer(read_only=True)
    holding_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingKassa.objects.all(), source='holding_kassa', write_only=True
    )

    class Meta:
        model = ShirketdenHoldingeTransfer
        fields = "__all__"
        read_only_fields = ('qalan_mebleg', 'evvelki_balans', 'sonraki_balans')


class OfisdenShirketeTransferSerializer(serializers.ModelSerializer):
    transfer_eden = serializers.StringRelatedField()
    transfer_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='transfer_eden', write_only=True, required=False, allow_null=True
    )
    ofis_kassa = OfisKassaSerializer(read_only=True)
    ofis_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=OfisKassa.objects.all(), source='ofis_kassa', write_only=True
    )
    shirket_kassa = ShirketKassaSerializer(read_only=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', write_only=True
    )

    class Meta:
        model = OfisdenShirketeTransfer
        fields = "__all__"
        read_only_fields = ('qalan_mebleg', 'evvelki_balans', 'sonraki_balans')

class ShirketdenOfislereTransferSerializer(serializers.ModelSerializer):
    transfer_eden = serializers.StringRelatedField()
    transfer_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='transfer_eden', write_only=True, required=False, allow_null=True
    )
    shirket_kassa = ShirketKassaSerializer(read_only=True)
    shirket_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=ShirketKassa.objects.all(), source='shirket_kassa', write_only=True
    )

    ofis_kassa = OfisKassaSerializer(read_only=True, many=True)
    ofis_kassa_id = serializers.PrimaryKeyRelatedField(
        queryset=OfisKassa.objects.all(), source='ofis_kassa', many=True,  write_only=True
    )

    class Meta:
        model = ShirketdenOfislereTransfer
        fields = "__all__"
        read_only_fields = ('qalan_mebleg', 'evvelki_balans', 'sonraki_balans')

