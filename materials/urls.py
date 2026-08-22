from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.class_list, name='class_list'),
    path('class/<int:class_id>/subjects/', views.subject_list, name='subject_list'),
    path('subject/<int:subject_id>/chapters/', views.chapter_list, name='chapter_list'),
    path('chapter/<int:chapter_id>/materials/', views.study_material_list, name='study_material_list'),
    path('material/<int:material_id>/', views.study_material_detail, name='study_material_detail'),
]
