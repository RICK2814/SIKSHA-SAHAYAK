from django.db import models

class ClassLevel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.class_level})"

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.title} - {self.subject}"

class StudyMaterial(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
