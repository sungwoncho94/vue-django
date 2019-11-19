from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Todo, User

# 사용자에게 이 정보를 담은 todo를 보내줄 것
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'user', 'title', 'completed',)


class UserDetailSerializer(serializers.ModelSerializer):
    todo_set = TodoSerializer(many=True)
    class Meta:
        model = User
        # 어떤 데이터를 보여주고 시리얼라이징, 디시리얼라이징 할지 정의
        fields = ('id', 'username', 'todo_set',)