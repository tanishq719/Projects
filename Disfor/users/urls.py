from django.urls import path
from . import views
from . views import UsersLoginView

urlpatterns = [
    path('register/', views.register),
    path('profile/',views.profile),
    # path('login/', views.login),
    path('login/', UsersLoginView.as_view(), name='obtain_token'),
    path('token/refresh/',views.refresh,name='refresh_token'),
    # path('token/verify/',MyTokenVerifyView.as_view(),name='verify_token')
    # path('token/delete/',TokenCookieDeleteView.as_view(), name='token_delete')
]
