from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ClassLevel, Subject, Chapter, StudyMaterial

@login_required
def class_list(request):
    classes = ClassLevel.objects.all()
    return render(request, 'materials/class_list.html', {'classes': classes})

@login_required
def subject_list(request, class_id):
    class_level = get_object_or_404(ClassLevel, id=class_id)
    subjects = class_level.subjects.all()
    return render(request, 'materials/subject_list.html', {
        'class_level': class_level,
        'subjects': subjects
    })

@login_required
def chapter_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    chapters = subject.chapters.all()
    return render(request, 'materials/chapter_list.html', {
        'subject': subject,
        'chapters': chapters
    })

@login_required
def study_material_list(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    materials = chapter.materials.all()
    return render(request, 'materials/study_material_list.html', {
        'chapter': chapter,
        'materials': materials
    })

@login_required
def study_material_detail(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    return render(request, 'materials/study_material_detail.html', {
        'material': material
    })
