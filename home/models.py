from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.title

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.slug = slugify(self.title)
        return super(Todo, self).save()
