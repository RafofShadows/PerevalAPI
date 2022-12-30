from django.urls import path, include
from rest_framework import routers

from userdata.views import submit_data, LevelViewSet, UserViewSet, PassDataViewSet, CoordsViewSet, ImageViewSet, \
    AreaViewSet, get_pass_data, patch_pass_data

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'perevals', PassDataViewSet)
router.register(r'coords', CoordsViewSet)
router.register(r'images', ImageViewSet)
router.register(r'areas', AreaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('submitdata/', submit_data),
    path('submitdata_get/<int:id>', get_pass_data),
    path('submitdata_patch/<int:id>', patch_pass_data),
]