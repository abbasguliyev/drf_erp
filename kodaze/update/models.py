from django.db import models

# Create your models here.
class Update(models.Model):
    update_name = models.CharField(max_length=150)
    update_description = models.TextField()
    update_version = models.CharField(max_length=100)

    class Meta:
        ordering = ("-pk",)

    # def __str__(self) -> str:
    #     return self.update_name