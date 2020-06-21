from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import json

class MyAuthentication(JWTAuthentication):

    def authenticate(self,request):
        header = self.get_header(request)
        if header is None:
            if settings.SIMPLE_JWT['JWT_TOKEN_COOKIE']:
                raw_token = json.loads(request.COOKIES.get(settings.SIMPLE_JWT['JWT_TOKEN_COOKIE_NAME']))['access']
                print(raw_token)
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
            else:
                return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token