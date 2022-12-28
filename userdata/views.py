from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
import json

from .models import User, Coords, Area, Image, PassData, Level
from .serializers import UserSerializer, AreaSerializer, CoordsSerializer, ImageSerializer, LevelSerializer, \
    PassDataSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PassDataViewSet(viewsets.ModelViewSet):
    queryset = PassData.objects.all()
    serializer_class = PassDataSerializer


@csrf_exempt
def submitData(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        user = UserSerializer(
            data={
                'email': json_data.get('user', {}).get('email'),
                'name': json_data.get('user', {}).get('name'),
                'fam': json_data.get('user', {}).get('fam'),
                'otc': json_data.get('user', {}).get('otc'),
                'phone': json_data.get('user', {}).get('phone'),
            }
        )

        coords = CoordsSerializer(
            data={
                'latitude': json_data.get('coords', {}).get('latitude'),
                'longitude': json_data.get('coords', {}).get('longitude'),
                'height': json_data.get('coords', {}).get('height'),
            }
        )

        level = LevelSerializer(
            data={
                'winter': json_data.get('level', {}).get('winter') if json_data.get('level', {}).get('winter') else '',
                'spring': json_data.get('level', {}).get('spring') if json_data.get('level', {}).get('spring') else '',
                'summer': json_data.get('level', {}).get('summer') if json_data.get('level', {}).get('summer') else '',
                'autumn': json_data.get('level', {}).get('autumn') if json_data.get('level', {}).get('autumn') else '',
            }
        )

        images = [ImageSerializer(
            data={
                'title': image_data.get('title'),
                'img': image_data.get('data'),
            }
        ) for image_data in json_data.get('images')]

        if not user.is_valid():
            return HttpResponse(
                json.dumps({'message': 'user is not valid'}),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST,
            )