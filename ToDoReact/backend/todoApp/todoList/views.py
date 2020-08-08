from todoList.models import TodoList, MyUser, TodoItem
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .serializers import UpdateUserSerializer, RegisterSerializer, LoginSerializer, UserSerializer, TodoListSerializer
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.db import transaction,connection


class DeleteTodo(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UpdateUserSerializer
    def post(self, request, *args, **kwargs):
        if(request.data['listId']):
            TodoList.objects.get(id=request.data['listId']).delete()
        elif(request.data['itemId']):
            TodoItem.objects.get(id=request.data['itemId']).delete()
        return Response({'msg':'deleted successfull!!'})

class AddTodoList(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UpdateUserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        print('{} {}'.format(request.data['priority'],request.data['listId']))
        if(not((request.data['listTitle'] or None) and request.data['priority']) and request.data['listId']):
            new_list = TodoList.objects.get(id=request.data['listId'])
            TodoItem.objects.create(parent_list=new_list,title=request.data['itemTitle'],description=request.data['description'],due_date=datetime.strptime(request.data['duedate'], '%d/%m/%Y'),isCompleted=False)
        else:
            l = self.request.user.has_todolist.create(title=request.data['listTitle'],priority=request.data['priority']=='true',isCompleted=False)
            new_list = TodoList.objects.get(title=l.title)
            TodoItem.objects.create(parent_list=new_list,title=request.data['itemTitle'],description=request.data['description'],due_date=datetime.strptime(request.data['duedate'], '%d/%m/%Y'),isCompleted=False)
        return Response({'msg':'added!!'})

class GetTodoList(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = TodoListSerializer

    def get_queryset(self):
        return self.request.user.has_todolist.all()

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            for u in MyUser.objects.all().values():
                print(u)
                data = list(TodoList.objects.filter(owner__id=u["id"]).values())
                for i,a in enumerate(data):
                    l = list(TodoItem.objects.filter(parent_list__id=a["id"]).values())
                    data[i]['items'] = l
                    data[i]['user'] = u["email"]
        else:
            data = list(TodoList.objects.filter(owner__id=request.user.id).values())
            for i,a in enumerate(data):
                l = list(TodoItem.objects.filter(parent_list__id=a["id"]).values())
                data[i]['items'] = l
                # data[i]['user'] = None

        return Response(data)

# class GetTodoListSet(viewsets.ModelViewSet):
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

#     print("inside")
#     serializer_class = TodoListSerializer

#     def get_queryset(self):
#         print("called")
#         return self.request.user.todolist.all()

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# is staff must be true only for the super user which is regarded as admin user here


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = MyUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "msg": "registered successfully"
        })


class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    print("before")
    queryset = MyUser.objects.all()
    print("after")

    def post(self, request, *args, **kwargs):
        print("before1")
        serializer = self.get_serializer(data=request.data)
        print("before2")
        print(request.data)
        serializer.is_valid(raise_exception=True)
        print("before3")
        user = serializer.validated_data

        d = {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.create(user=user),
            "login":True
        }
        print(d)
        return Response(d)
