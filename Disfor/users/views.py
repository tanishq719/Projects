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
from django.middleware import csrf
from django.conf import settings as ST
from rest_framework_simplejwt.tokens import RefreshToken
import json

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

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def profile(request):
    return Response({'data':'successfully identified'},status=200)

# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def login(request):
#     if request.method == 'POST':
#         serializer = MyUserLoginSerializer(data=request.data)
#         data = {}

#         if serializer.is_valid():
#             data['response'] = "Logged in Successfully!!"
#             token = RefreshToken.for_user(serializer)

#             if ST.SIMPLE_JWT['JWT_TOKEN_COOKIE']:
#                 expiration = (datetime.utcnow()+ST.SIMPLE_JWT['CSRF_COOKIE_EXPIRY'])
#                 response.set_cookie(ST.SIMPLE_JWT['JWT_TOKEN_COOKIE_NAME'],
#                                     token,
#                                     httponly=True)
#             else:
#                 pass
#             return Response(data)
#         else:
#             data = serializer.errors
#             return Response(data,status=422)

class UsersLoginView(TokenObtainPairView):
    serializer_class = UsersLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = serializer.validated_data
        print(data)
        if data['access'] :
            if ST.SIMPLE_JWT['JWT_TOKEN_COOKIE']:
                csrf.get_token(request)     #this here is only setting token in request header
                                            # latter middleware will add cookie for it in response
                response = Response({'msg':'logged in successfully'},status=200)
                response.set_cookie(ST.SIMPLE_JWT['JWT_TOKEN_COOKIE_NAME'],
                                    json.dumps(obj=data),
                                    httponly=True)
            else:
                response = Response({'access':data['access'],'refresh':data['refresh']}, status=200)
        else:
            response = Response(data,status=422)
        return response

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = UsersLoginSerializer

class MyTokenVerifyView(TokenVerifyView):
    serializer_class = UsersLoginSerializer