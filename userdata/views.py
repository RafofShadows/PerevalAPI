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

        email = json_data.get('user', {}).get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first
        else:
            user = UserSerializer(
                data={
                    'email': json_data.get('user', {}).get('email'),
                    'name': json_data.get('user', {}).get('name'),
                    'fam': json_data.get('user', {}).get('fam'),
                    'otc': json_data.get('user', {}).get('otc'),
                    'phone': json_data.get('user', {}).get('phone'),
                }
            )
            if user.is_valid():
                user = user.save()
            else:
                return HttpResponse(
                    json.dumps({'message': 'Недопустимый пользователь'}),
                    content_type="application/json",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        coords = CoordsSerializer(
            data={
                'latitude': json_data.get('coords', {}).get('latitude'),
                'longitude': json_data.get('coords', {}).get('longitude'),
                'height': json_data.get('coords', {}).get('height'),
            }
        )

        if not coords.is_valid():
            return HttpResponse(
                json.dumps({'message': 'Недопустимые координаты'}),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST,
            )

        level = LevelSerializer(
            data={
                'winter': json_data.get('level', {}).get('winter') if json_data.get('level', {}).get('winter') else '',
                'spring': json_data.get('level', {}).get('spring') if json_data.get('level', {}).get('spring') else '',
                'summer': json_data.get('level', {}).get('summer') if json_data.get('level', {}).get('summer') else '',
                'autumn': json_data.get('level', {}).get('autumn') if json_data.get('level', {}).get('autumn') else '',
            }
        )

        if not level.is_valid():
            return HttpResponse(
                json.dumps({'message': 'Недопустимая категория трудности'}),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST,
            )

        images = [ImageSerializer(
            data={
                'title': image_data.get('title'),
                'img': image_data.get('data'),
            }
        ) for image_data in json_data.get('images')]

        for image in images:
            if not image.is_valid():
                return HttpResponse(
                    json.dumps({'message': 'Недопустимое изображение'}),
                    content_type="application/json",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        pass_data = PassData.objects.create(
            beauty_title=json_data.get('beauty_title'),
            title=json_data.get('title'),
            other_titles=json_data.get('other_titles'),
            user=user,
            coords=coords.save(),
            levels=level.save(),
            status='new',
            )

        if pass_data:
            pass_data.images.add([image.save() for image in images])
            pass_data.save()

        response_data = {
            'id': pass_data.pk
        }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=status.HTTP_201_CREATED,
        )
