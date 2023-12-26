from django.db import models

class LikeManager(models.Manager):
    def like_pos(self):
        return self.filter(like__gt=0)

    def like_neg(self):
        return self.filter(like__lt=0)

    def like_zero(self):
        return self.filter(like=0)

class QuestionManager(LikeManager):
    pass

class AnswerManager(LikeManager):
    def correct(self):
        return self.filter(is_correct=True)

    def not_correct(self):
        return self.filter(is_correct=False)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    photo = models.ImageField(upload_to="img/")
    tags = models.ManyToManyField(Tag, related_name='questions')
    like = models.IntegerField()

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title}"

class Answer(models.Model):
    content = models.TextField(blank=False)
    is_correct = models.BooleanField(blank=True)
    what_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    like = models.IntegerField()

    objects = AnswerManager()

    def __str__(self):
        return f"{self.content[:30]}..."
