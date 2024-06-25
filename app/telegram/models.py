from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"


class History(models.Model):
    telegram_id = models.BigIntegerField()
    action = models.CharField(max_length=255)
    message_text = models.CharField(max_length=255, default="")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.telegram_id} - {self.action} at {self.date_created}"
