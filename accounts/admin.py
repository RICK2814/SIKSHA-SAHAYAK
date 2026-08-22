from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'class_level']
    list_filter = ['class_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
