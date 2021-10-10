from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from task.views import TaskView, UserView, AuthView, TasksUser

router = DefaultRouter()
router.register('task', TaskView)
router.register('user', UserView)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api-auth/', include('rest_framework.urls')),

   path('api/', include(router.urls)),
   path('api-token-auth/', obtain_jwt_token),
   path('api-token-refresh/', refresh_jwt_token),
   path('api-token-verify/', verify_jwt_token),
   path('registration/', AuthView.as_view()),
   path('api/task_user/<int:user_id>/', TasksUser.as_view()),
]
