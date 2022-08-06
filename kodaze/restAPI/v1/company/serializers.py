from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import (
    User
)

from company.models import (
    Holding,
    Shirket,
    Ofis,
    Komanda,
    Shobe,
    VezifePermission,
    Vezifeler
)
from django.contrib.auth.models import Group


class VezifeUserSerializer(serializers.ModelSerializer):
    """
    Bu Seriazlier UserEmeliyyatSeriazlier-de vezifeleri istifade etmek ucun istifade olunur
    """
    class Meta:
        model = Vezifeler
        fields = ['vezife_adi']

class UserEmeliyyatSerializer(serializers.ModelSerializer):
    """
    Bu Seriazlier Kassa Emeliyyatlarinda User-in(transferi eden ishcinin) melumatlarini gostermek ucun istifade olur
    """
    vezife = VezifeUserSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['asa', 'vezife']


class ShirketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shirket
        fields = "__all__"

    def create(self, validated_data):
        shirket_adi = validated_data.get('shirket_adi')
        validated_data['shirket_adi'] = shirket_adi.upper()
        try:
            return super(ShirketSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail": 'Bu ad ilə şirkət artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.shirket_adi = validated_data.get('shirket_adi', instance.shirket_adi).upper()
        instance.holding = validated_data.get('holding', instance.holding)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class KomandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komanda
        fields = "__all__"

    def create(self, validated_data):
        komanda_adi = validated_data.get('komanda_adi')
        validated_data['komanda_adi'] = komanda_adi.upper()
        try:
            k = Komanda.objects.filter(komanda_adi=komanda_adi.upper(), is_active=True)
            if len(k) > 0:
                raise ValidationError
            return super(KomandaSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail": 'Bu ad ilə komanda artıq əlavə olunub'})


class OfisSerializer(serializers.ModelSerializer):
    shirket = ShirketSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True
    )

    class Meta:
        model = Ofis
        fields = "__all__"

    def create(self, validated_data):
        ofis_adi = validated_data.get('ofis_adi')
        validated_data['ofis_adi'] = ofis_adi.upper()
        shirket = validated_data['shirket']
        print(f"{shirket=}")
        try:
            ofiss = Ofis.objects.filter(ofis_adi=ofis_adi.upper(), shirket=shirket)
            print(f"{ofiss=}")
            if len(ofiss)>0:
                raise ValidationError
            return super(OfisSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail": 'Bu ad ilə ofis artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.ofis_adi = validated_data.get('ofis_adi', instance.ofis_adi).upper()
        instance.shirket = validated_data.get('shirket', instance.shirket)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class ShobeSerializer(serializers.ModelSerializer):
    ofis = OfisSerializer(read_only=True)
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True
    )

    class Meta:
        model = Shobe
        fields = "__all__"

    def create(self, validated_data):
        shobe_adi = validated_data.get('shobe_adi')
        validated_data['shobe_adi'] = shobe_adi.upper()
        ofis = validated_data['ofis']
        print(f"{ofis=}")
        try:
            shobe_qs = Ofis.objects.filter(shobe_adi=shobe_adi.upper(), ofis=ofis)
            print(f"{shobe_qs=}")
            if len(shobe_qs)>0:
                raise ValidationError
            return super(ShobeSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail": 'Bu ad ilə şöbə artıq əlavə olunub'})

class VezifelerSerializer(serializers.ModelSerializer):
    shobe = ShobeSerializer(read_only=True, required=False)
    shirket = ShirketSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True
    )

    class Meta:
        model = Vezifeler
        fields = "__all__"

    def create(self, validated_data):
        vezife_adi = validated_data.get('vezife_adi')
        validated_data['vezife_adi'] = vezife_adi.upper()
        return super(VezifelerSerializer, self).create(validated_data)

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = "__all__"

    def create(self, validated_data):
        holding_adi = validated_data.get('holding_adi')
        validated_data['holding_adi'] = holding_adi.upper()
        try:
            return super(HoldingSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail": 'Bu ad ilə holding artıq əlavə olunub'})

class VezifePermissionSerializer(serializers.ModelSerializer):
    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source='vezife', write_only=True
    )

    permission_group = serializers.StringRelatedField(read_only=True)
    permission_group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='permission_group', write_only=True, allow_null=True
    )

    class Meta:
        model = VezifePermission
        fields = '__all__'
