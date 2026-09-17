from django.db import models


# Custom User model for storing user registration details
class User(models.Model):

    # Username will be generated automatically during signup
    username = models.CharField(
        max_length=150,       # Maximum number of characters
        unique=True,          # Username must be unique
        blank=True            # Username can be empty when creating the user
    )

    # User's first name
    first_name = models.CharField(
        max_length=100
    )

    # User's middle name
    # null=True allows NULL in the database
    # blank=True makes this field optional in forms
    middle_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    # User's last name
    last_name = models.CharField(
        max_length=100
    )

    # User's date of birth
    date_of_birth = models.DateField()

    # User's email address
    # unique=True prevents duplicate email addresses
    email = models.EmailField(
        unique=True
    )

    # User's mobile number
    # unique=True prevents duplicate mobile numbers
    mobile_number = models.CharField(
        max_length=15,
        unique=True
    )

    # User's location/address
    location = models.CharField(
        max_length=255
    )

    # User's postal/pincode
    pincode = models.CharField(
        max_length=10
    )

    # User's password
    # The password should be stored as a hashed value
    password = models.CharField(
        max_length=128
    )

    # Automatically stores the date and time
    # when the user is first created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Defines how the User object is displayed
    def __str__(self):
        return self.email