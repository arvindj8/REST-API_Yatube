
from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostModelViewSet)
router.register(r'posts/(?P<id>\d+)/comments', views.CommentModelViewSet)
router.register(r'groups', views.GroupReadOnlyModelViewSet)
router.register(r'follow', views.FollowModelViewSet)

app_name = 'api_v1'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
