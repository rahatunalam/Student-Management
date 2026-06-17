from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20,unique=True)
    email = models.CharField(unique=True)
    class_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

class Mark(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='marks')
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5,decimal_places=2)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.score}"
    
    def get_grade(self):
        if self.score >= 80:
            return 'A+'
        elif self.score >= 70:
            return 'A'
        elif self.score >= 60:
            return 'B'
        elif self.score >= 50:
            return 'C'
        elif self.score >= 40:
            return 'D'
        else:
            return 'F'