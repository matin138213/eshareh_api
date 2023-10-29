from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('words', views.WordViewSet, basename='words'),
router.register('category', views.CategoryViewSet, basename='category'),
urlpatterns = router.urls