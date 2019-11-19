from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import TodoSerializer, UserDetailSerializer
from .models import Todo
# 특정 methods의 요청만 허용하겠다를 정해줌
from rest_framework.decorators import api_view
from rest_framework.response import Response
User = get_user_model()


@api_view(['POST'])  # 특정 메소드의 요청만 허용
def todo_create(request):
    # request.data 는 axios의 body로 전달한 데이터임
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # 사용자가 새롭게 작성한 데이터를 응답해준다
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def todo_update_delete(request, todo_id):
    # 수정하거나 삭제할 todo instance 호출
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == "PUT":
        # todo를 수정할건데, data로 수정할거에요! 라는 뜻
        # instance todo를 request.data로 넘어온 값으로 수정할 것
        serializer = TodoSerializer(instance=todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    if request.method == "DELETE":
        todo.delete()
        # 204 : 삭제했다는 코드  ->  요청에 성공했찌만 컨텐츠는 없다는걸 알려주는 status code
        return Response(status=204)


@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserDetailSerializer(instance=user)
    return Response(serializer.data)
