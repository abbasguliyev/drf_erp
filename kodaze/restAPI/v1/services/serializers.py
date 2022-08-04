from rest_framework import serializers

from contract.models import (
    Muqavile, 
)
from services.models import (
    Servis, 
    ServisOdeme, 
)

from product.models import (
    Mehsullar, 
)

from restAPI.v1.contract.serializers import MuqavileSerializer
from restAPI.v1.product.serializers import MehsullarSerializer

class ServisSerializer(serializers.ModelSerializer):
    muqavile = MuqavileSerializer(read_only=True)
    mehsullar = MehsullarSerializer(read_only=True, many=True)

    muqavile_id = serializers.PrimaryKeyRelatedField(
        queryset=Muqavile.objects.all(), source='muqavile', write_only=True, required=False, allow_null=True
    )
    mehsullar_id = serializers.PrimaryKeyRelatedField(
        queryset=Mehsullar.objects.all(), source='mehsullar', many=True, write_only=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    class Meta:
        model = Servis
        fields = "__all__"

class ServisStatistikaSerializer(serializers.ModelSerializer):
    muqavile = MuqavileSerializer(read_only=True)
    mehsullar = MehsullarSerializer(read_only=True, many=True)

    muqavile_id = serializers.PrimaryKeyRelatedField(
        queryset=Muqavile.objects.all(), source='muqavile', write_only=True, required=False, allow_null=True
    )
    mehsullar_id = serializers.PrimaryKeyRelatedField(
        queryset=Mehsullar.objects.all(), source='mehsullar', many=True, write_only=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        endirim = 0
        endirim += float(instance.endirim)
        try:
            endirim_faizi = (endirim * 100) / float(instance.odenilecek_umumi_mebleg)
        except:
            endirim_faizi = 0
        representation['endrim_faizi'] = endirim_faizi

        return representation

    class Meta:
        model = Servis
        fields = "__all__"

class ServisOdemeSerializer(serializers.ModelSerializer):
    servis = ServisSerializer(read_only=True)
    servis_id = serializers.PrimaryKeyRelatedField(
        queryset=Servis.objects.all(), source='servis', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ServisOdeme
        fields = "__all__"

