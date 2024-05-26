from django.contrib import admin

from core.models import Course, Chapter, Task, Question, Answer, CourseComment, TaskResult, CourseResult, QuestionResult


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(CourseComment)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskResult)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(CourseResult)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestionResult)
class AnswerAdmin(admin.ModelAdmin):
    pass