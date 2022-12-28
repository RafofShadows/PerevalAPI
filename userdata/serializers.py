import io

from django.core.files.images import ImageFile
from rest_framework import serializers

from .models import User, Coords, Area, Image, PassData, Level


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            return User.objects.create(
                email=self.validated_data.get('email'),
                name=self.validated_data.get('name'),
                fam=self.validated_data.get('fam'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
            )


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

    # def save(self, **kwargs):
    #     self.is_valid()
    #     area = Area.objects.filter(title=self.validated_data.get('title'))
    #     if area.exists():
    #         return area.first()
    #     else:
    #         return Area.objects.create(
    #             parent=self.validated_data.get('parent'),
    #             title=self.validated_data.get('title'),
    #         )


class ImageSerializer(serializers.Serializer):
    image_char = serializers.CharField(max_length=20000000)
    title = serializers.CharField()

    def save(self, **kwargs):
        image_bytes = bytes.fromhex(self.validated_data['image_char'])
        image = ImageFile(io.BytesIO(image_bytes), name=f'{self.validated_data["title"]}.jpg')
        return Image.objects.create(image=image, title=self.validated_data["title"])


class PassDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassData
        fields = '__all__'
        depth = 1


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


