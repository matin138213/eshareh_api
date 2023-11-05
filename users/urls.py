from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users'),
router.register('interest',views.InterestViewSet,basename='interest'),
urlpatterns = router.urls
