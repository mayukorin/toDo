from django.db import models
from todo_app.models.siteUser import SiteUser
from django.utils import timezone


class Task(models.Model):

    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(default=timezone.now, blank=True, null=True)
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, default=None)
    done_flag = models.BooleanField(null=True)

    def __str__(self):
        return self.title
