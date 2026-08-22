from django.contrib import admin
from .models import Question, Quiz, QuizQuestion, QuizAttempt, StudentAnswer, PracticeAttempt

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'chapter', 'difficulty', 'correct_answer']
    list_filter = ['chapter__subject__class_level', 'chapter__subject', 'difficulty']
    search_fields = ['question_text']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'time_limit', 'total_marks', 'created_at']
    list_filter = ['chapter__subject__class_level', 'chapter__subject']
    search_fields = ['title']
    inlines = [QuizQuestionInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'total_questions', 'percentage', 'completed_at']
    list_filter = ['quiz__chapter__subject__class_level']
    search_fields = ['student__username']

@admin.register(PracticeAttempt)
class PracticeAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'question', 'is_correct', 'attempted_at']
    list_filter = ['is_correct']
