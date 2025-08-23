from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.date}" 