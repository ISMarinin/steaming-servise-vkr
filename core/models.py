from pathlib import Path
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
import os
from django.core.validators import MaxValueValidator, MinValueValidator

BASE_DIR = Path(__file__).resolve().parent.parent


class CourseCategory(models.TextChoices):
    ENGLISH = 'English'
    MATH = 'Math'
    OTHER = 'Other'

class TaskCategory(models.TextChoices):
    CHOOSE_ANSWERS = 'CHOOSE_ANSWERS'
    WRITE_ANSWERS = 'WRITE_ANSWERS'

class Course(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FilePathField(path= os.path.join(BASE_DIR, 'static/img'),)
    category = models.CharField(
        max_length=60,
        choices=CourseCategory.choices,
        default=CourseCategory.OTHER,
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    numberOfUsers = models.IntegerField()
    pass_threshhold = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    single_attempt_course = models.BooleanField()
    def __str__(self):
        return f"{self.title}"

class CourseComment(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return f"Comment - author:{self.author} - date:{self.date}"

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    theoreticatPart = models.TextField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}"

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=60,
        choices=TaskCategory.choices,
        default=TaskCategory.CHOOSE_ANSWERS,

    )
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.description}"
class Question(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    description = models.TextField()
    tip = models.CharField(max_length=120 ,blank=True)
    def __str__(self):
        return f"{self.description}"

class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.answer}"

class TaskResult(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

class QuestionResult(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    task_result = models.ForeignKey(to=TaskResult, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answer = models.TextField()
    given_answer = models.TextField()

class CourseResult(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    pass_threshhold = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])

    def __str__(self):
        return f"CourseUserProgress - course:{self.course} - user:{self.user}"

