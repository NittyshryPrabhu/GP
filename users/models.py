from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):

    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # 🔥 NEW FIELDS
    mobile = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    subscription = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='free'
    )

    def __str__(self):
        return self.user.username
