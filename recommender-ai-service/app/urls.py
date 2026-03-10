from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)

urlpatterns = router.urls
