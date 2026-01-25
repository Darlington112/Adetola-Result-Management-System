from django.db import models

# Create your models here.

class Class(models.Model):
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=20)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.class_name} - {self.section}"
    

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.subject_name} - {self.subject_code}"
    

class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    name = models.CharField(max_length=100)
    roll_id = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob = models.CharField(max_length=50)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)


    def __str__(self):
        return self.name
    

class SubjectCombination(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
   


    def __str__(self):
        return f"{self.student_class} - {self.subject}"
    


    
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    test_marks = models.IntegerField(default=0)

    exam_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0,editable=False)

    grade = models.CharField(max_length=2, blank=True)
    status = models.CharField(max_length=4, blank=True)  # Pass / Fail

    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.test_marks = int(self.test_marks)
        self.exam_marks = int(self.exam_marks)

        # Total
        self.total_marks = self.test_marks + self.exam_marks

        # Grade
        if self.total_marks >= 75:
            self.grade = 'A1'
        elif self.total_marks >= 70:
            self.grade = 'B2'
        elif self.total_marks >= 65:
            self.grade = 'B3'
        elif self.total_marks >= 60:
            self.grade = 'C4'
        elif self.total_marks >= 55:
            self.grade = 'C5'
        elif self.total_marks >= 50:
            self.grade = 'C6'
        elif self.total_marks >= 45:
            self.grade = 'D7'
        elif self.total_marks >= 40:
            self.grade = 'E8'
        else:
            self.grade = 'F'

        # Pass / Fail
        self.status = 'Pass' if self.total_marks >= 39 else 'Fail'

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.student} - {self.subject} | "
            f"Total: {self.total_marks}, "
            f"Grade: {self.grade}, "
            f"Status: {self.status}"
        )

class Notice(models.Model):
   title = models.CharField(max_length=200)
   details = models.TextField()
   posting_date = models.DateTimeField(auto_now_add=True)
   updation_date = models.DateTimeField(auto_now=True)
   
    
def __str__(self):
        return self.title


    


 