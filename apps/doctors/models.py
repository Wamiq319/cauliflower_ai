from django.db import models
from django.conf import settings

class GeneralSuggestion(models.Model):
    DISEASE_CHOICES = [
        ("black_rot", "Black Rot"),
        ("downy_mildew", "Downy Mildew"),
        ("bacterial_spot", "Bacterial Spot"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    title = models.CharField(max_length=255)
    treatment = models.TextField()
    prevention = models.TextField()
    best_practices = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_disease_type_display()})"
