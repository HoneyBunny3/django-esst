from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    #on_delete=models.CASCADE means if a user is deleted all notes associated with them is also deleted!
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    