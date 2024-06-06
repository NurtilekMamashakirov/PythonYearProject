from django.db import models


# Create your models here.
class Link(models.Model):
    url = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class Chat(models.Model):
    id = models.IntegerField(primary_key=True)
    links = models.ManyToManyField(Link)

    def __str__(self):
        return str(self.id)
