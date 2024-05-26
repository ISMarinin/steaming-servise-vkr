
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from core.models import CourseResult
from users.forms import CustomUserCreationForm

import logging

logger = logging.getLogger(__name__)

def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        course_results = CourseResult.objects.filter(user=request.user)
        context.update({'course_results': course_results})
    return render(request, "dashboard.html", context=context)


def register(request):
    if request.method == "GET":
        return render(
            request, "register.html", {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            logger.error("Форма не валидна")