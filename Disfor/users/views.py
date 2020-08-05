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
from rest_framework_simplejwt.views import TokenObtainPairView
from django.middleware import csrf
from django.conf import settings as ST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
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

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def profile(request):
    return Response({'data':'successfully identified'},status=200)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def refresh(request):
    if request.method == 'POST':
        try:
            raw_token = request.data['access_token']
            print(raw_token)
            cookie_token = json.loads(request.COOKIES.get(ST.SIMPLE_JWT['JWT_HTTPONLY_TOKEN_COOKIE_NAME']))
            print(cookie_token)
            if cookie_token['access'] == raw_token:
                refresh = RefreshToken(cookie_token['refresh'])
                data = {'access': json.dumps(str(refresh.access_token))}
                response = Response({'access':data['access'],'msg':'Successfully gained token'},status=200)
                response.set_cookie(ST.SIMPLE_JWT['JWT_HTTPONLY_TOKEN_COOKIE_NAME'],
                                        json.dumps(obj={'refresh':json.dumps(str(refresh)),'access':data['access']}),
                                        httponly=True,
                                        samesite='Lax',
                                        path='/users/token')
                response['credentials'] = 'same-origin'
                response['Access-Control-Allow-Credentials'] = 'true'
            else:
                response = Response({'msg':'NOT ALLOWED, Try again or Login again'}, status=403)
        except:
            print('Error..')
            response = Response({'msg':'Server side error, Try Again...'}, status=403)
        finally:
            return response
            


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
                # csrf.get_token(request)     #this here is only setting token in request header
                                            # latter middleware will add cookie for it in response
                response = Response({'access':data['access'],'user':data['user'],'msg':'logged in successfully'},status=200)
                response.set_cookie(ST.SIMPLE_JWT['JWT_HTTPONLY_TOKEN_COOKIE_NAME'],
                                    json.dumps(obj={key: data[key] for key in ('refresh','access')}),
                                    httponly=True,
                                    samesite='Lax',
                                    path='/users/token')
                
                response['credentials'] = 'same-origin'
                response['Access-Control-Allow-Credentials'] = 'true'
            else:
                response = Response({'data':data}, status=200)
        else:
            response = Response(data,status=422)
        return response

