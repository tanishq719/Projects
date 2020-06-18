from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from . models import Users
from . serializers import UsersRegistrationSerializer, UsersLoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

@api_view(['POST'])
# @parser_classes([MultiPartParser])
@permission_classes((permissions.AllowAny,))
def register(request):
    print('enter')
    if request.method == 'POST':
        print('before')
        serializer = UsersRegistrationSerializer(data=request.data)
        print(request.data)
        # print(request.files)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            data['response'] = "successfully registered!!"
            return Response(data)
        else:
            data = serializer.errors
            return Response(data,status=422)

class UsersLoginView(TokenObtainPairView):
    serializer_class = UsersLoginSerializer

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = UsersLoginSerializer

class MyTokenVerifyView(TokenVerifyView):
    serializer_class = UsersLoginSerializer