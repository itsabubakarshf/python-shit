from django.db import models

class ImageModel(models.Model):
    data = models.TextField()
    class Meta:
        app_label="app"
