from rest_framework.routers import DefaultRouter

from accounts.api.views.user import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
