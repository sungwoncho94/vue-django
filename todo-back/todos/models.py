from django.db import models
# 유저 모델을 새롭게 작성하기 위해 abstractUser 상속받아서 씀
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# AbstractUser를 사용할건데, 그대로 상속받아서 쓸 것. (default 유저를 사용하더라도 장고에서는 강력히 커스텀 유저를 사용하라고 권장)
class User(AbstractUser):
    pass


class Todo(models.Model):
    # user.todos.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

