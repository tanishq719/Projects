from rest_framework import serializers
from todoList.models import TodoList, TodoItem, MyUser
from django.contrib.auth import authenticate
from django.db import transaction


class TodoItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    isCompleted = serializers.BooleanField(required=False)
    class Meta:
        model = TodoItem
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'isCompleted'
        ]

class TodoListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    isCompleted = serializers.BooleanField(required=False)
    class Meta:
        model = TodoList
        fields = [
            'id',
            'title',
            'priority',
            'isCompleted'
        ]

class UpdateUserSerializer(serializers.ModelSerializer):
    has_todolist = TodoListSerializer(many=True)
    items = TodoItemSerializer(many=True)

    class Meta:
        model = MyUser
        fields = ['has_todolist','items']

    # @transaction.atomic
    def create(self,validated_data):
        todolist = validated_data.pop('has_todolist')
        items_data = validated_data.pop('items')
        users = MyUser.objects.values()
        obj = {}
        print(users)
        for u in users:
            if u["id"] == self.context['request'].user.id:
                for todo in todolist:
                    t = TodoList(owner=MyUser.objects.get(id=u["id"]),**todo)
                    t.save(force_insert=True)
                    transaction.commit()
                    for item in items_data:
                        obj = TodoItem(parent_list=t,**item)
                        obj.save(force_insert=True)
                        transaction.commit()
        
        return obj

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('password','email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'],
                                        validated_data['password'])

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email','is_staff')


# username
# admin123@todo.com
# admin123
 