from django.db import models

class Student(models.Model):
# Student Details
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    dob = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    course = models.CharField(max_length=100)
    roll_no = models.CharField(
    max_length=20,
    unique=True,
    null=True,
    blank=True
    )

    # Parent Details
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    parent_contact = models.CharField(max_length=15, blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    # Address Details
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    # Academic Details
    obtained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)

    # Photo
    image = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    # Record Date
    created_at = models.DateTimeField(
    auto_now_add=True,
    null=True,
    blank=True
    )

    def percentage(self):
        if self.total_marks > 0:
            return round(
                (self.obtained_marks / self.total_marks) * 100,
                2
            )
        return 0

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

