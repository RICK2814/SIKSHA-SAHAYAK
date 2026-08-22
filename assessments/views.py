from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q
from materials.models import Subject, Chapter
from .models import Question, Quiz, QuizQuestion, QuizAttempt, StudentAnswer, PracticeAttempt
from accounts.models import StudentProfile
import json

@login_required
def practice_questions(request, chapter_id=None):
    chapter = None
    if chapter_id:
        chapter = get_object_or_404(Chapter, id=chapter_id)
        questions = Question.objects.filter(chapter=chapter)
    else:
        profile = StudentProfile.objects.filter(user=request.user).first()
        if profile and profile.class_level:
            subjects = Subject.objects.filter(class_level=profile.class_level)
            chapters = Chapter.objects.filter(subject__in=subjects)
            questions = Question.objects.filter(chapter__in=chapters)
        else:
            questions = Question.objects.all()

    # Get already attempted questions
    attempted_ids = PracticeAttempt.objects.filter(
        student=request.user,
        question__in=questions
    ).values_list('question_id', flat=True)

    # Filter unattempted or show all
    show_all = request.GET.get('all', False)
    if not show_all:
        questions = questions.exclude(id__in=attempted_ids)

    questions = questions.order_by('?')[:10]  # Random 10 questions

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_answer = request.POST.get('answer')
        question = get_object_or_404(Question, id=question_id)
        is_correct = (selected_answer == question.correct_answer)
        PracticeAttempt.objects.create(
            student=request.user,
            question=question,
            selected_answer=selected_answer,
            is_correct=is_correct
        )
        return render(request, 'assessments/practice_result.html', {
            'question': question,
            'selected_answer': selected_answer,
            'is_correct': is_correct,
            'chapter': chapter
        })

    question = questions.first() if questions.exists() else None
    return render(request, 'assessments/practice_questions.html', {
        'question': question,
        'chapter': chapter,
        'total_available': questions.count()
    })

@login_required
def quiz_list(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if profile and profile.class_level:
        subjects = Subject.objects.filter(class_level=profile.class_level)
        chapters = Chapter.objects.filter(subject__in=subjects)
        quizzes = Quiz.objects.filter(chapter__in=chapters)
    else:
        quizzes = Quiz.objects.all()

    # Get attempt counts
    for quiz in quizzes:
        quiz.attempts_count = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
        latest = QuizAttempt.objects.filter(student=request.user, quiz=quiz).order_by('-completed_at').first()
        quiz.latest_score = latest.percentage if latest else None

    return render(request, 'assessments/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.quiz_questions.select_related('question').all()
    attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz).order_by('-completed_at')[:5]
    return render(request, 'assessments/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'attempts': attempts
    })

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_questions = quiz.quiz_questions.select_related('question').order_by('order')

    if request.method == 'POST':
        # Process quiz submission
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            total_questions=quiz_questions.count()
        )

        score = 0
        for qq in quiz_questions:
            selected = request.POST.get(f'question_{qq.question.id}')
            is_correct = (selected == qq.question.correct_answer) if selected else False
            if is_correct:
                score += qq.marks
            StudentAnswer.objects.create(
                attempt=attempt,
                question=qq.question,
                selected_answer=selected or '',
                is_correct=is_correct
            )

        attempt.score = score
        attempt.percentage = round((score / quiz.total_marks) * 100, 2) if quiz.total_marks > 0 else 0
        attempt.completed_at = timezone.now()
        attempt.save()

        messages.success(request, f'Quiz submitted! You scored {score}/{quiz.total_marks}')
        return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, 'assessments/take_quiz.html', {
        'quiz': quiz,
        'quiz_questions': quiz_questions
    })

@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    answers = attempt.answers.select_related('question').all()
    return render(request, 'assessments/quiz_result.html', {
        'attempt': attempt,
        'answers': answers
    })

@login_required
def my_progress(request):
    quiz_attempts = QuizAttempt.objects.filter(student=request.user)
    practice_attempts = PracticeAttempt.objects.filter(student=request.user)

    total_quizzes = quiz_attempts.count()
    completed_quizzes = quiz_attempts.filter(completed_at__isnull=False).count()
    avg_score = quiz_attempts.filter(completed_at__isnull=False).aggregate(Avg('percentage'))['percentage__avg'] or 0
    highest_score = quiz_attempts.filter(completed_at__isnull=False).order_by('-percentage').first()

    total_questions = practice_attempts.count()
    correct_answers = practice_attempts.filter(is_correct=True).count()
    accuracy = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0

    # Topics completed (chapters with all materials viewed - simplified)
    profile = StudentProfile.objects.filter(user=request.user).first()
    subjects = []
    if profile and profile.class_level:
        subjects = Subject.objects.filter(class_level=profile.class_level)

    recent_attempts = quiz_attempts.filter(completed_at__isnull=False).order_by('-completed_at')[:10]

    return render(request, 'assessments/my_progress.html', {
        'total_quizzes': total_quizzes,
        'completed_quizzes': completed_quizzes,
        'avg_score': round(avg_score, 2),
        'highest_score': highest_score,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'subjects': subjects,
        'recent_attempts': recent_attempts
    })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from materials.models import Subject, Chapter, StudyMaterial
from assessments.models import QuizAttempt, PracticeAttempt
from accounts.models import StudentProfile

@login_required
def dashboard(request):
    profile = StudentProfile.objects.filter(user=request.user).first()

    # Get subjects for student's class
    subjects = []
    if profile and profile.class_level:
        subjects = Subject.objects.filter(class_level=profile.class_level)

    # Progress stats
    quiz_attempts = QuizAttempt.objects.filter(student=request.user, completed_at__isnull=False)
    quizzes_attempted = quiz_attempts.count()
    avg_score = quiz_attempts.aggregate(Avg('percentage'))['percentage__avg'] or 0

    practice_attempts = PracticeAttempt.objects.filter(student=request.user)
    questions_attempted = practice_attempts.count()
    correct_answers = practice_attempts.filter(is_correct=True).count()

    # Topics completed - count chapters that have study materials
    topics_completed = 0
    if profile and profile.class_level:
        topics_completed = Chapter.objects.filter(
            subject__class_level=profile.class_level
        ).count()

    context = {
        'profile': profile,
        'subjects': subjects,
        'quizzes_attempted': quizzes_attempted,
        'avg_score': round(avg_score, 2),
        'topics_completed': topics_completed,
        'questions_attempted': questions_attempted,
        'correct_answers': correct_answers,
    }
    return render(request, 'dashboard/dashboard.html', context)
