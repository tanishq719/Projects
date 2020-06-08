from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from . models import Users
from . serializers import UsersRegistrationSerializer

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    
    if request.method == 'POST':
        serializer = UsersRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered!!"
            # decide whether the user should login after registration or not
            # also if not to login then whether whole object should be shared or except password
        else:
            data = serializer.errors
        return Response(data)