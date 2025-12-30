from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    designation = models.CharField(max_length=150)
    education = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)

    resume = models.FileField(upload_to="resumes/")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    



class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('fulltime', 'Full-time'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES)
    

    skill_1 = models.CharField(max_length=100)
    skill_2 = models.CharField(max_length=100, blank=True, null=True)
    skill_3 = models.CharField(max_length=100, blank=True, null=True)
    skill_4 = models.CharField(max_length=100, blank=True, null=True)
    skill_5 = models.CharField(max_length=100, blank=True, null=True)

    experience = models.CharField(max_length=100, blank=True, null=True)
    vacancies = models.PositiveIntegerField(default=1)
    required_qualification = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='posted_jobs')  

   

    def __str__(self):
        return f"{self.title} at {self.company}"
    



class JobApplication(models.Model):
    candidate = models.ForeignKey('User', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='applied')
    notes = models.TextField(blank=True, null=True)  

    class Meta:
        unique_together = ('candidate', 'job') 

    def __str__(self):
        return f"{self.candidate.email} -> {self.job.title}"




