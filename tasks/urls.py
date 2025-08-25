from django.urls import path
from .views import TaskListCreateView,TaskDetailView,signup_view,logout_view,delete_account_view,ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('api/tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('api/task/<int:id>/', TaskDetailView.as_view(), name='task_detail'),
    path('api/signup/', signup_view, name='signup_api' ),
    path('api/token/', obtain_auth_token, name='token_api'),
    path('api/logout/', logout_view, name='logout_api'),
    path('api/delete/account/', delete_account_view, name='delete_account'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password' )
]