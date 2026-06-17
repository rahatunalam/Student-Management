from django import forms
from .models import Student,Mark

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','roll_no','email','class_name']
        widgets = {
            'name':       forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Enter full name'}),
            'roll_no':    forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'e.g 21225103**'}),
            'email':      forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Enter email'}),
            'class_name': forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'e.g Intake 40'}),
        }

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject','score','exam_date']
        weidgets = {
            'subjects': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Mathematics'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'0-100'}),
            'exam_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }
