from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Users
from . serializers import UsersSerializer

@api_view(['POST'])
def register(request):
    TOKEN = 0
    serializer = UsersSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(TOKEN, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)