from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('users', views.UserlViewSet, basename='users'),
router.register('interest',views.InterestViewSet,basename='interest'),
urlpatterns = router.urls
