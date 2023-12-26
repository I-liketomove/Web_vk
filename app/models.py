from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db.models import Count, Q


class LikeManager(models.Manager):
    def like_pos(self):
        return self.filter(like__gt=0)

    def like_neg(self):
        return self.filter(like__lt=0)

    def like_zero(self):
        return self.filter(like=0)

class QuestionManager(LikeManager):
    pass

class TagManager(models.Manager):
    pass

class UserManager(BaseUserManager):
    def best_users(self, amount):
        return self.annotate(correct_answers_count=Count('answer', filter=Q(answer__is_correct=True))).order_by(
                '-correct_answers_count')[:amount]


class AnswerManager(LikeManager):
    def correct(self):
        return self.filter(is_correct=True)

    def not_correct(self):
        return self.filter(is_correct=False)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = TagManager()

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    photo = models.ImageField(null=True, blank=True, default="avatars/anon.png")
    nickname = models.CharField('User Nickname', max_length=50, default='user')
    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set")

    objects = UserManager()

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    photo = models.ImageField(upload_to="img/")
    tags = models.ManyToManyField(Tag, related_name='questions')
    like = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title}"

class Answer(models.Model):
    content = models.TextField(blank=False)
    is_correct = models.BooleanField(blank=True)
    what_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.content[:30]}..."
