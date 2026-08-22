from django.contrib import admin
from .models import ClassLevel, Subject, Chapter, StudyMaterial

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_level']
    list_filter = ['class_level']
    search_fields = ['name']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'order']
    list_filter = ['subject__class_level', 'subject']
    search_fields = ['title']
    ordering = ['order']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'created_at']
    list_filter = ['chapter__subject__class_level', 'chapter__subject']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
