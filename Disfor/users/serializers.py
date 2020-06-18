from users.models import Users
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
import json

class UsersRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = Users
        fields = ['username','first_name','last_name','join_date','email',
                'last_login','reputation','password','like_count',
                'dislike_count','reply_count','description','dp','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'two passwords are not matching'})
        
        user = Users(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            join_date=datetime.now(),
            email=self.validated_data['email'],
            last_login=datetime.now(),
            reputation=0,
            password=Users.get_hashed(self.validated_data['password']),
            like_count=0,
            dislike_count=0,
            reply_count=0,
            description=self.validated_data['description'],
            dp = self.validated_data['dp']
        )

        user.save()
        return user

class UsersLoginSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls,user):
    #     token = super().get_token(user)
    #     print(user)
    #     token['name'] = user['username']  #getting username OrderedDict([('username', 'akki21'), ('password', 'bhaikaandroidnahichala')])

    #     return token

    def validate(self, attrs):
        users = Users.objects.filter(username = attrs['username']).values()
        print(users)

        if not (users and Users.verify_password(raw_password= attrs['password'],hash_password = users[0]['password'])):
            raise serializers.ValidationError("No user exists with provided credentials")

        user = Users.get_object(users[0])
        refresh = self.get_token(user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        image_file = json.dumps(str(user.dp))
        data['user'] = {'username':user.username,'first_name':user.first_name,'last_name':user.last_name,
                        'join_date':user.join_date, 'email':user.email, 'last_login':user.last_login,
                        'reputation':user.reputation, 'like_count':user.like_count, 'dislike_count':user.dislike_count,
                        'reply_count':user.reply_count, 'description':user.description, 'dp':image_file}

        return data