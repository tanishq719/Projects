from users.models import Users
from rest_framework import serializers
from datetime import datetime

class UsersRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = Users
        fields = ['username','first_name','last_name','join_date','email',
                'last_active_date','reputation','password','like_count',
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
            last_active_date=datetime.now(),
            reputation=0,
            password=self.validated_data['password'],
            like_count=0,
            dislike_count=0,
            reply_count=0,
            description=self.validated_data['description'],
            dp = self.validated_data['dp']
        )

        user.save()
        return user