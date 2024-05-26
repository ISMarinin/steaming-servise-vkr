# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("landing-index/", views.landing_index, name="landing_index"),
    path("course-index/", views.course_index, name="course_index"),
    path("course-detail/<int:pk>/", views.course_detail, name="course_detail"),
    path("course-enrollment/<int:pk>/", views.course_enrollment, name="course_enrollment"),
    path("course-drop-progress/<int:pk>/", views.course_drop_progress, name="course_drop_progress"),
    path("task/<int:pk>/", views.task, name="task"),
    path("recommend/simular/", views.recommend_simular, name="recommend_simular"),
]