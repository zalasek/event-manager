from django.db import models
import uuid

class Event(models.Model):
    microservices = (
        ('users', 'users'),
        ('products', 'products'),
        ('revievs', 'revievs'),
        ('comments', 'comments'),
        ('files', 'files'),
        ('messages', 'messages'),
    )
    
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key=True,default = uuid.uuid4)
    source = models.CharField(max_length=20,choices=microservices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    description = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

