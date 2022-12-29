from django.urls import path, include
from rest_framework import routers

from userdata.views import submit_data, LevelViewSet, UserViewSet, PassDataViewSet, CoordsViewSet, ImageViewSet, \
    AreaViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'perevals', PassDataViewSet)
router.register(r'coords', CoordsViewSet)
router.register(r'images', ImageViewSet)
router.register(r'areas', AreaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('submitdata/', submit_data)
]