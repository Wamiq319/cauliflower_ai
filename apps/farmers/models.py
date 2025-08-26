from django.db import models
from django.conf import settings
from django.utils import timezone

def case_image_path(instance, filename):
    """Generate file path for case images"""
    return f'cases/{instance.farmer.id}/{timezone.now().strftime("%Y%m%d")}/{filename}'

class Analysis(models.Model):
    """Model to store plant disease analysis results"""
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses')
    image = models.ImageField(upload_to=case_image_path)
    crop_name = models.CharField(max_length=100)
    disease_name = models.CharField(max_length=100)
    analysis_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-analysis_date']
    
    def __str__(self):
        return f"{self.farmer.username} - {self.crop_name} - {self.disease_name}"

class Case(models.Model):
    """Model to store cases opened by farmers for doctor review"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Case #{self.id} - {self.farmer.username} - {self.status}"

class CaseSuggestion(models.Model):
    """Model to store suggestions from different doctors for a case"""
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='suggestions')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='case_suggestions')
    title = models.CharField(max_length=255)
    treatment = models.TextField()
    prevention = models.TextField()
    best_practices = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=Case.PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Suggestion by {self.doctor.username} for Case #{self.case.id}" 