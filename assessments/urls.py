from django.urls import path
from . import views

urlpatterns = [
    path('practice/', views.practice_questions, name='practice_questions'),
    path('practice/chapter/<int:chapter_id>/', views.practice_questions, name='practice_chapter'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('progress/', views.my_progress, name='my_progress'),
]
