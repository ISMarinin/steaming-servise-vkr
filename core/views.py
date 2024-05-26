import random

from django.http import Http404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Case, When

from core.forms import CommentForm
from core.models import Course, Task, Question, Answer, CourseResult, TaskResult, QuestionResult

import logging
import pandas as pd

logger = logging.getLogger(__name__)
def landing_index(request):
    return render(request, 'landing_index.html')

def course_index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course_index.html', context)

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Anonimus'

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.course = course
            new_comment.author = username
            new_comment.save()
            comments = course.coursecomment_set.all()
            sum = 0
            for comment in comments:
                sum += comment.rating
            course.rating = round(sum / comments.count(), 2)
            course.save()
    else:
        comment_form = CommentForm()

    course_result = CourseResult.objects.filter(user=request.user).filter(course=course)
    if course_result:
        course_result = course_result[0]
        counter = 0
        score = 0
        for chapter in course.chapter_set.all():
            for task in chapter.task_set.all():
                counter += 1
                if TaskResult.objects.filter(user=request.user).filter(task=task):
                    score += 1
        course_result.score = round(score / counter * 100)

        if course_result.score == 100:
            questions = 0
            questions_correct = 0
            for chapter in course.chapter_set.all():
                for task in chapter.task_set.all():
                    task_result = TaskResult.objects.filter(user=request.user).filter(task=task)[0]
                    for question_result in QuestionResult.objects.filter(user=request.user).filter(task_result=task_result):
                        questions += 1
                        if question_result.given_answer == question_result.correct_answer:
                            questions_correct += 1
            course_result.pass_threshhold = round(questions_correct / questions * 100)
        course_result.save()

    context = {
        'course': course,
        'comment_form': comment_form,
        "course_result": course_result
    }
    return render(request, 'course_detail.html', context)

@login_required
def course_enrollment(request, pk):
    course = Course.objects.get(pk=pk)
    course_result = CourseResult.objects.filter(user=request.user).filter(course=course)
    if not course_result:
        CourseResult.objects.create(course=course, user= request.user, score=0)
    context = {
        'course': course
    }
    return render(request, 'course_enrollment.html', context)

@login_required
def task(request, pk):
    task = Task.objects.get(pk=pk)
    task_result = TaskResult.objects.filter(user=request.user).filter(task=task)
    context = {
        'task': task,
        'course': task.chapter.course,
    }

    if task_result:
        task_result = task_result[0]
        question_results = task_result.questionresult_set.all()
        context.update({"question_results": question_results})
        context.update({"task_result": task_result})
        return render(request, 'task_results.html', context)
    else:
        if request.method == 'POST':
            questions = []
            data = request.POST
            data_ = dict(data.lists())
            data_.pop('csrfmiddlewaretoken')
            for k in data_.keys():
                question = Question.objects.get(description=k)
                questions.append(question)
            question_results = []
            correct_answer = None
            score = 0
            task_result = TaskResult.objects.create(task=task, user=request.user, score=0)
            for q in task.question_set.all():
                if q not in questions:
                    questions.append(q)
            for q in questions:
                a_selected = request.POST.get(q.description)

                questions_answers = Answer.objects.filter(question=q)
                for a in questions_answers:
                    if a.correct:
                        correct_answer = a.answer
                if a_selected is None:
                    a_selected = ""
                question_result = QuestionResult.objects.create(question=q, user=request.user, correct_answer=correct_answer,
                                                                    task_result=task_result, given_answer=a_selected)
                question_results.append(question_result)
                if question_result.given_answer == question_result.correct_answer:
                    score += 1

            task_result.score = round(score / len(question_results), 2) * 100
            task_result.save()

            context.update({"question_results": question_results})
            context.update({"task_result": task_result})
            return render(request, 'task_results.html', context)

        else:
            questions = []
            for q in task.question_set.all():
                answers = []
                for a in q.answer_set.all():
                    answers.append(a.answer)
                questions.append({str(q): answers})
            random.shuffle(questions)
            context.update({"questions": questions})
            return render(request, 'task.html', context)

def course_drop_progress(request, pk):
    course = Course.objects.get(pk=pk)
    CourseResult.objects.get(course_id=pk, user=request.user).delete()
    for chapter in course.chapter_set.all():
        for task in chapter.task_set.all():
            taskResult = TaskResult.objects.filter(task=task, user=request.user)
            if taskResult:
                taskResult[0].delete()
            for question in task.question_set.all():
                questionResult = QuestionResult.objects.filter(question=question, user=request.user)
                if questionResult:
                    questionResult[0].delete()

    return redirect(reverse('course_detail', kwargs={'pk':pk}))


def get_similar(course_id,score,corrMatrix):
    similar_scores = corrMatrix[course_id]*(score-2.5)
    similar_scores = similar_scores.sort_values(ascending=False)
    return similar_scores

@login_required
def recommend_simular(request):

    course_result_rating=pd.DataFrame(list(CourseResult.objects.all().values()))

    userRatings = course_result_rating.pivot_table(index=['user_id'],columns=['course_id'],values='score')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(CourseResult.objects.filter(user=request.user).values())).drop(['user_id','id','pass_threshhold'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    courses_passed_ids = [each[0] for each in user_filtered]

    similar_course = pd.DataFrame()
    for course, score in user_filtered:
        similar_course = similar_course.append(get_similar(course, score, corrMatrix), ignore_index = True)

    couse_ids = list(similar_course.sum().sort_values(ascending=False).index)
    course_ids_recommend = [each for each in couse_ids if each not in courses_passed_ids]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(course_ids_recommend)])
    course_list = list(Course.objects.filter(id__in = course_ids_recommend).order_by(preserved)[:1])

    context = {'courses': course_list}
    return render(request, 'recommend-simular.html', context)
