from django.db import models


class User(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    location = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email