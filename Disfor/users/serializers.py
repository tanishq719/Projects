from users.models import Users
from rest_framework import serialzers

class UsersSerializer(serialzers.ModelSerializer):
    class Meta:
        model = Users

    fields = '__all__'
    