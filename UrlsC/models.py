from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Urls(models.Model):
    original_url = models.URLField()
    shortened_url = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)  # Define si la URL es privada o pública
    view_count = models.PositiveIntegerField(default=0)  # Número de vistas
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Usuario que creó la URL
    created_at = models.DateTimeField(auto_now_add=True)
  

    def __str__(self):
        return self.original_url
    
