from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import django
from account.models import (
    IsciSatisSayi,
    MusteriQeydler,
    User,
    Musteri,
    Bolge,
    IsciStatus
)
from restAPI.v1.company.serializers import (
    ShirketSerializer,
    OfisSerializer,
    ShobeSerializer,
    KomandaSerializer,
    VezifelerSerializer
)

from company.models import (
    Shirket,
    Ofis,
    Komanda,
    Shobe,
    VezifePermission,
    Vezifeler
)

from django.contrib.auth.models import Permission, Group
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class IsciStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsciStatus
        fields = "__all__"

    def create(self, validated_data):
        status_adi = validated_data.get('status_adi')
        validated_data['status_adi'] = status_adi.upper()
        return super(IsciStatusSerializer, self).create(validated_data)


class BolgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolge
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password reset endpoint.
    """
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    shobe = serializers.PrimaryKeyRelatedField(
        queryset=Shobe.objects.all(), required=True)
    shirket = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), required=True)
    ofis = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), required=True)
    vezife = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), required=True)
    tel1 = serializers.CharField(required=True)

    ishe_baslama_tarixi = serializers.DateField(format="%d-%m-%Y", required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'asa', 'dogum_tarixi',
            'tel1', 'tel2', 'sv_image', 'sv_image2', 'shirket', 'isci_status',
            'ofis', 'vezife', 'komanda', 'user_permissions', 'groups', 'profile_image',
            'maas', 'qeyd', 'shobe', 'maas_uslubu', 'elektron_imza', 'password', 'password2','ishe_baslama_tarixi'
        )

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if data['shobe'] == None:
            raise serializers.ValidationError(
                {"password": "Şöbəni daxil edin"})
        if data['shirket'] == None:
            raise serializers.ValidationError(
                {"password": "Şirkəti daxil edin"})
        if data['ofis'] == None:
            raise serializers.ValidationError({"password": "Ofisi daxil edin"})
        if data['vezife'] == None:
            raise serializers.ValidationError(
                {"password": "Vəzifə daxil edin"})
        if data['tel1'] == None:
            raise serializers.ValidationError(
                {"password": "Ən az 1 telefon nömrəsi daxil edin"})

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   asa=validated_data['asa'], dogum_tarixi=validated_data['dogum_tarixi'],
                                   tel1=validated_data['tel1'], tel2=validated_data['tel2'], komanda=validated_data['komanda'],
                                   isci_status=validated_data['isci_status'], vezife=validated_data['vezife'],
                                   qeyd=validated_data['qeyd'],
                                   shirket=validated_data['shirket'], ofis=validated_data['ofis'],
                                   shobe=validated_data['shobe'], sv_image=validated_data['sv_image'],
                                   maas_uslubu=validated_data['maas_uslubu']
                                   )
        user.set_password(validated_data['password'])
        try:
            user.sv_image2 = validated_data['sv_image2']
        except:
            user.sv_image2 = None

        try:
            user.profile_image = validated_data['profile_image']
        except:
            user.profile_image = None

        try:
            user.elektron_imza = validated_data['elektron_imza']
        except:
            user.elektron_imza = None

        try:
            user.ishe_baslama_tarixi = validated_data['ishe_baslama_tarixi']
        except:
            user.ishe_baslama_tarixi = django.utils.timezone.now()

        if validated_data['maas'] == None:
            user.maas = 0
        elif validated_data['maas'] is not None:
            user.maas = validated_data['maas']

        vezife = validated_data['vezife']
        vezife_permission = VezifePermission.objects.filter(vezife=vezife)
        print(f"{vezife_permission=}")
        if vezife_permission is not None:
            for vp in vezife_permission:
                permission_group = vp.permission_group
                print(f"{permission_group=}")
                user.groups.add(permission_group)

        user_permissions = validated_data['user_permissions']
        for user_permission in user_permissions:
            user.user_permissions.add(user_permission)

        # vezife_permission = get_object_or_404(VezifePermission, )
        groups = validated_data['groups']
        for group in groups:
            user.groups.add(group)

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    shirket = ShirketSerializer(read_only=True)
    ofis = OfisSerializer(read_only=True)
    shobe = ShobeSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True,
    )
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True
    )
    shobe_id = serializers.PrimaryKeyRelatedField(
        queryset=Shobe.objects.all(), source='shobe',
        write_only=True, required=False, allow_null=True
    )

    vezife = VezifelerSerializer(read_only=True)
    vezife_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source='vezife', write_only=True,
    )

    komanda = KomandaSerializer(read_only=True)
    komanda_id = serializers.PrimaryKeyRelatedField(
        queryset=Komanda.objects.all(), source='komanda', write_only=True,
    )

    isci_status = IsciStatusSerializer(read_only=True)
    isci_status_id = serializers.PrimaryKeyRelatedField(
        queryset=IsciStatus.objects.all(), source='isci_status', write_only=True,
    )

    user_permissions = PermissionSerializer(read_only=True, many=True)
    user_permissions_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='user_permissions', write_only=True, many=True
    )

    ishden_cixma_tarixi = serializers.DateField(read_only=True)

    class Meta:
        model = User
        exclude = ('password',)

    def update(self, instance, validated_data):
        user = instance
        user_permissions = validated_data.get('user_permissions')
        print(f"{user_permissions=}")
        if user_permissions is not None:
            for user_permission in user_permissions:
                user.user_permissions.add(user_permission)

        instance.save()
        return super().update(instance, validated_data)


class MusteriSerializer(serializers.ModelSerializer):
    bolge = BolgeSerializer(read_only=True)
    bolge_id = serializers.PrimaryKeyRelatedField(
        queryset=Bolge.objects.all(), source="bolge", write_only=True
    )

    class Meta:
        model = Musteri
        fields = "__all__"


class MusteriQeydlerSerializer(serializers.ModelSerializer):
    musteri = MusteriSerializer(read_only=True)

    musteri_id = serializers.PrimaryKeyRelatedField(
        queryset=Musteri.objects.all(), source='musteri', write_only=True
    )

    class Meta:
        model = MusteriQeydler
        fields = "__all__"


class IsciSatisSayiSerializer(serializers.ModelSerializer):
    isci = UserSerializer(read_only=True)
    isci_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='isci', write_only=True
    )

    class Meta:
        model = IsciSatisSayi
        fields = "__all__"
