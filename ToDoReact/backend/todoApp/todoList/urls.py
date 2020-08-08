from rest_framework import routers
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterAPI, LoginAPI, GetTodoList, AddTodoList, DeleteTodo

# router = routers.DefaultRouter()
# router.register('api/todo/getTodos/', GetTodoListSet, 'todolist')
# router.register('api/auth/register/', RegisterAPI.as_view(), 'user')
# router.register('api/auth/login/',LoginAPI.as_view(), 'user')
#logout

# urlpatterns = router.urls
urlpatterns = [
    path('api/auth/addUser/',RegisterAPI.as_view(),name='addUser'),
    path('api/todo/deleteTodo/',DeleteTodo.as_view(),name='deleteTodo'),
    path('api/todo/addTodoList/',AddTodoList.as_view(),name='assTodoList'),
    path('api/todo/getTodos/',GetTodoList.as_view(),name='getTodos'),
    path('api/auth/register/',RegisterAPI.as_view(), name='register'),
    path('api/auth/login/',obtain_auth_token, name='login')
]
