from django.contrib import admin
from .models import Student,Mark

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'email', 'class_name', 'created_at')
    search_fields = ('name' , 'roll_no', 'email')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student','subject','score','exam_date')
    search_fields = ('student__name','subject')
    
