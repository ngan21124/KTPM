from rest_framework.routers import DefaultRouter
from .views import StaffViewSet

router = DefaultRouter()
router.register(r'staff', StaffViewSet)

urlpatterns = router.urls
