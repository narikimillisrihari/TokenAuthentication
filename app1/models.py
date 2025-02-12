from django.db import models
# from django.contrib.auth import use

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=250)
    year=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    creator=models.ForeignKey('auth.User',related_name='movies',on_delete=models.CASCADE)

    class Meta:
        ordering=['-id']
