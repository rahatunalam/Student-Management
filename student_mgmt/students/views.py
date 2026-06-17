from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student,Mark
from .forms import StudentForm,MarkForm
from django.db.models import Avg


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,f'Welcome Back,{user.username}!')

            if not user.is_staff and hasattr(user,'student_profile'):
                return redirect('student_detail',pk=user.student_profile.pk)
            
            return redirect('student_list')
        else:
            messages.error(request,'Invalid username or password!')

    return render(request, 'students/login.html')

# Logout View
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,'You have been logged out.')
        return redirect('login')
    return redirect('student_list')

@login_required
# List all students.
def student_list(request):

    if not request.user.is_staff and hasattr(request.user, 'student_profile'):
        return redirect('student_detail', pk=request.user.student_profile.pk)

    search = request.GET.get('search','')
    class_filter = request.GET.get('class_filter','')

    students = Student.objects.all().order_by('-created_at')

    if search:
        from django.db.models import Q
        students = students.filter(
            Q(name__icontains=search)|
            Q(roll_no__icontains=search)
        )
    
    if class_filter:
        students = students.filter(class_name__icontains=class_filter)

    from django.core.paginator import Paginator
    paginator = Paginator(students,5)

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    all_classes = Student.objects.values_list('class_name',flat=True).distinct()
    
    return render(request, 'students/student_list.html', {
        'students': students,
        'page_obj': page_obj,
        'search': search,
        'class_filter': class_filter,
        'all_classes': all_classes,
        })

# Create a new student
def student_create(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request, 'students/student_form.html',{'form':form, 'title': 'Add Student'})

# Edit an existing student 
def student_edit(request,pk):
    student = get_object_or_404(Student,pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request, 'students/student_form.html',{'form':form,'title': 'Edit Student'})
 
# Delete a student
def student_delete(request,pk):
    student = get_object_or_404(Student,pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request , 'students/student_confirm_delete.html',{'student': student})

# Student detail/Grade report page
@login_required
def student_detail(request,pk):
    student = get_object_or_404(Student, pk=pk)

    if not request.user.is_staff and hasattr(request.user, 'student_profile'):
        if request.user.student_profile.pk != student.pk:
            messages.error(request, 'You can only view your own profile.')
            return redirect('student_list')
        
    marks = student.marks.all().order_by('exam_date')
    average = marks.aggregate(Avg('score')).get('score__avg') or 0
    return render(request,'students/student_detail.html',{
        'student': student,
        'marks': marks,
        'average': round(average,2)
    })

# Add mark for a student
@login_required
def add_mark(request,pk):
    if not request.user.is_staff:
        messages.error(request,'You don not have permission to add marks.')
        return redirect('student_list')
    
    student = get_object_or_404(Student,pk=pk)
    form = MarkForm()

    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.student = student
            mark.save()
            messages.success(request,f'Mark added for {student.name}!')
            return redirect('student_detail',pk=student.pk)
        
    return render(request,'students/mark_form.html',{
        'form': form,
        'student': student,
    })

# EDIT MARK
@login_required
def edit_mark(request, pk):
    # Only admin/staff can edit marks
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit marks.')
        return redirect('student_list')

    # Get the mark object itself (not the student)
    mark = get_object_or_404(Mark, pk=pk)

    if request.method == 'POST':
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mark updated successfully!')
            return redirect('student_detail', pk=mark.student.pk)
    else:
        # Pre-fill the form with the existing mark's data
        form = MarkForm(instance=mark)

    return render(request, 'students/mark_form.html', {
        'form':    form,
        'student': mark.student,
        'edit':    True,  # flag used in template to change the title/button text
    })


# DELETE MARK
@login_required
def delete_mark(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete marks.')
        return redirect('student_list')

    mark = get_object_or_404(Mark, pk=pk)
    student_pk = mark.student.pk  # save this before deleting, we need it for redirect

    if request.method == 'POST':
        mark.delete()
        messages.success(request, 'Mark deleted successfully!')
        return redirect('student_detail', pk=student_pk)

    return render(request, 'students/mark_confirm_delete.html', {'mark': mark})