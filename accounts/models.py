from django.db import models
from django.contrib.auth.models import User
from materials.models import ClassLevel

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.class_level}"
