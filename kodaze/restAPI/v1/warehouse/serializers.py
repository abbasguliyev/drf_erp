from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from warehouse.models import (
    Emeliyyat, 
    Anbar, 
    AnbarQeydler, 
    Stok,
)
from product.models import (
    Mehsullar, 
)

from account.models import (
    User, 
)

from company.models import (
    Shirket,
    Ofis,
)

from restAPI.v1.account.serializers import UserSerializer
from restAPI.v1.product.serializers import MehsullarSerializer

from restAPI.v1.company.serializers import OfisSerializer, ShirketSerializer

class AnbarSerializer(serializers.ModelSerializer):
    shirket = ShirketSerializer(read_only=True)
    ofis = OfisSerializer(read_only=True)
    shirket_id = serializers.PrimaryKeyRelatedField(
        queryset=Shirket.objects.all(), source='shirket', write_only=True
    )
    ofis_id = serializers.PrimaryKeyRelatedField(
        queryset=Ofis.objects.all(), source='ofis', write_only=True
    )

    class Meta:
        model = Anbar
        fields = "__all__"

    def create(self, validated_data):
        ad = validated_data.get('ad')
        validated_data['ad'] = ad.upper()
        try:
            return super(AnbarSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu ad ilə anbar artıq əlavə olunub'})

class EmeliyyatSerializer(serializers.ModelSerializer):
    gonderen = AnbarSerializer(read_only=True)
    qebul_eden = AnbarSerializer(read_only=True)

    gonderen_id = serializers.PrimaryKeyRelatedField(
        queryset=Anbar.objects.all(), source="gonderen", write_only=True, required= True
    )
    qebul_eden_id = serializers.PrimaryKeyRelatedField(
        queryset=Anbar.objects.all(), source="qebul_eden", write_only=True, required= True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        mehsul_ve_sayi = instance.mehsul_ve_sayi
        print(f"{mehsul_ve_sayi=}")
        data = dict()
        if(mehsul_ve_sayi is not None):
            mehsul_ve_sayi_list = mehsul_ve_sayi.split(",")
            print(f"{mehsul_ve_sayi_list=}")

            

            for m in mehsul_ve_sayi_list:
                mehsul_ve_say = m.split("-")
                print(f"{mehsul_ve_say=}--- {type(mehsul_ve_say)=}")
                mehsul_id = int(mehsul_ve_say[0].strip())
                say = int(mehsul_ve_say[1])
                print(f"{mehsul_id=}")
                print(f"{say=}")
                mehsul = Mehsullar.objects.get(pk=mehsul_id)
                data[mehsul.mehsulun_adi]=say

        representation['mehsul'] = data

        return representation

    class Meta:
        model = Emeliyyat
        fields = "__all__"

class StokSerializer(serializers.ModelSerializer):
    anbar = AnbarSerializer(read_only=True)
    mehsul = MehsullarSerializer(read_only=True)

    anbar_id = serializers.PrimaryKeyRelatedField(
        queryset=Anbar.objects.all(), source='anbar', write_only=True
    )

    mehsul_id = serializers.PrimaryKeyRelatedField(
        queryset=Mehsullar.objects.all(), source='mehsul', write_only=True
    )
    
    class Meta:
        model = Stok
        fields = "__all__"


class AnbarQeydlerSerializer(serializers.ModelSerializer):
    anbar = AnbarSerializer(read_only=True)
    anbar_id = serializers.PrimaryKeyRelatedField(
        queryset=Anbar.objects.all(), source='anbar', write_only=True
    )

    gonderen_user = UserSerializer(read_only=True)
    gonderen_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='gonderen_user', write_only=True, required=False, allow_null=True
    )

    stok = StokSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        mehsul_ve_sayi = instance.mehsul_ve_sayi
        print(f"{mehsul_ve_sayi=}")
        stok_list = list()
        
        if(mehsul_ve_sayi is not None):
            mehsul_ve_sayi_list = mehsul_ve_sayi.split(",")
            print(f"{mehsul_ve_sayi_list=}")

            for m in mehsul_ve_sayi_list:
                stok_data = dict()
                mehsul_ve_say = m.split("-")
                print(f"{mehsul_ve_say=}--- {type(mehsul_ve_say)=}")
                mehsul_id = int(mehsul_ve_say[0].strip())
                say = int(mehsul_ve_say[1])
                print(f"{mehsul_id=}")
                print(f"{say=}")
                mehsul = Mehsullar.objects.get(pk=mehsul_id)
                try:
                    stok = Stok.objects.filter(mehsul=mehsul, anbar=instance.anbar)[0]
                    stok_data['id'] = stok.id
                    stok_data['mehsul_id'] = stok.mehsul.id
                    stok_data['mehsul'] = stok.mehsul.mehsulun_adi
                    stok_data['qiymet'] = stok.mehsul.qiymet
                    stok_data['say'] = stok.say
                    stok_data['miqdari'] = say
                    stok_list.append(stok_data)
                except:
                    stok_list.append(stok_data)
        
        representation['mehsul'] = stok_list

        return representation

    class Meta:
        model = AnbarQeydler
        fields = "__all__"
        read_only_fields = ('gonderen_user', 'stok')