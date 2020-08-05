from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.response import Response

class MyAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except:
            validated_token = self.regenerateTokenIfNotAnAttack(request,raw_token)
        return Response(status=200),self.get_user(validated_token), validated_token

    def regenerateTokenIfNotAnAttack(self,request,raw_token):
        if json.loads(request.COOKIES.get(settings.JWT_HTTPONLY_TOKEN_COOKIE_NAME)['access']) == raw_token:
            refresh = RefreshToken(attrs['refresh'])

            data = {'access': str(refresh.access_token)}

            if api_settings.ROTATE_REFRESH_TOKENS:
                if api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        # Attempt to blacklist the given refresh token
                        refresh.blacklist()
                    except AttributeError:
                        # If blacklist app not installed, `blacklist` method will
                        # not be present
                        pass

                refresh.set_jti()
                refresh.set_exp()

                data['refresh'] = str(refresh)
            return data['access']
    # def authenticate(self,request):
    #     header = self.get_header(request)
    #     if header is None:
    #         if settings.SIMPLE_JWT['JWT_REFRESH_TOKEN_COOKIE']:
    #             # print(request.COOKIES.get(settings.SIMPLE_JWT['JWT_TOKEN_COOKIE_NAME']))
    #             raw_token = json.loads(request.COOKIES.get(settings.SIMPLE_JWT['JWT_REFRESH_TOKEN_COOKIE_NAME']))['access']
    #             # print(raw_token)
    #             validated_token = self.get_validated_token(raw_token)
    #             return self.get_user(validated_token), validated_token
    #         else:
    #             return None

    #     raw_token = self.get_raw_token(header)
    #     if raw_token is None:
    #         return None

    #     validated_token = self.get_validated_token(raw_token)

    #     return self.get_user(validated_token), validated_token