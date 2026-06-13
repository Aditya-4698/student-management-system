from django.db import models
from django.utils import timezone

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



class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=100)

    isbn = models.CharField(max_length=50, unique=True)

    category = models.CharField(max_length=100)

    publisher = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    available_quantity = models.PositiveIntegerField()

    shelf_no = models.CharField(max_length=50)

    book_image = models.ImageField(
        upload_to='books/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IssueBook(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()

    status = models.CharField(max_length=20, default='Issued')

    fine_per_day = 10  # ₹10 per day late

    def is_overdue(self):
        if self.status == "Returned":
            return False
        return timezone.now().date() > self.return_date

    def fine_amount(self):
        if not self.is_overdue():
            return 0
        days = (timezone.now().date() - self.return_date).days
        return days * self.fine_per_day