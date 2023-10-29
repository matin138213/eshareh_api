from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('exams', views.ExamViewSet, basename='exams'),
router.register('sentences',views.SentenceViewSet,basename='sentences'),
urlpatterns = router.urls
