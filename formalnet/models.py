from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Prompts(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author =models.ForeignKey(User,on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.input_text} -> {self.output_text}"

