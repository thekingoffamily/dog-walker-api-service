from django.db import models
import uuid
from django.contrib.postgres.fields import JSONField

class WalkOrder(models.Model):
    apartment_number = models.PositiveIntegerField()
    pet_name = models.CharField(max_length=100)
    pet_breed = models.CharField(max_length=100)
    walk_datetime = models.DateTimeField()
    walker = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.apartment_number} - {self.pet_name} - {self.walk_datetime}"

class APICall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=50)
    data = models.JSONField()  # Используйте JSONField из django.db.models
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.timestamp}"