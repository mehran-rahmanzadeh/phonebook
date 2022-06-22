from rest_framework.routers import DefaultRouter

from contacts.api.views.contact import ContactViewSet
from contacts.api.views.group import GroupViewSet

router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'group', GroupViewSet, basename='group')

urlpatterns = router.urls
