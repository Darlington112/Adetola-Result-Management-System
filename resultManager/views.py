from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    notices = Notice.objects.all().order_by('id')
    return render(request, 'index.html', locals())

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice_detail.html', locals())

def admin_login(request):
    if request.user.is_authenticated:
        return redirect( 'admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)

            return redirect('admin_dashboard')
        else:
            error = {'error': 'Invalid credentials or not an admin user.'}
            
    return render(request, 'admin_login.html', locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_classes = Class.objects.count()
    total_results = Result.objects.values('student').distinct().count()
    return render(request, 'admin_dashboard.html', locals())


def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def create_class(request):
    if request.method == 'POST':
        try:
           class_name = request.POST.get('class_name')
           section = request.POST.get('section')
          
           Class.objects.create(class_name=class_name, section=section)  
           messages.success(request, "Class created successfully.")
           return redirect(create_class)

        except Exception as e:
            messages.error(request, f"Error creating class.{str(e)}")  
            return redirect(create_class)
  
    return render(request, 'create_class.html')


@login_required(login_url='admin_login')
def manage_classes(request):

    # Fetch all classes from database
    classes = Class.objects.all()

    if request.GET.get('delete'):
        # Handle deletion of a class
        try:
            class_id = request.GET.get('delete')
            class_obj = get_object_or_404(Class, id=class_id)
            class_obj.delete()
            messages.success(request, "Class deleted successfully.")
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            return redirect('manage_classes')
    return render(request, 'manage_classes.html', locals())


@login_required(login_url='admin_login')
def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_numeric = request.POST.get('class_name_numeric')
        section = request.POST.get('section')
        try:
           class_obj.class_name = class_name
           class_obj.class_numeric = class_numeric
           class_obj.section = section
       
        
           class_obj.save()

           messages.success(request, "Class updated successfully.")
           return redirect(manage_classes)

        except Exception as e:
            messages.error(request, f"Error updating class.{str(e)}")  
            return redirect(manage_classes)

    
  
    return render(request, 'edit_class.html', locals())



@login_required(login_url='admin_login')
def create_subject(request):
    if request.method == 'POST':
        try:
           subject_name = request.POST.get('subject_name')
           subject_code = request.POST.get('subject_code')
          
           Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
           messages.success(request, "Subject created successfully.")

        except Exception as e:
            messages.error(request, f"Error creating Subject.{str(e)}")  
            return redirect(create_subject)
    return render(request, 'create_subject.html')

@login_required(login_url='admin_login')
def manage_subject(request):

    # Fetch all classes from database
    subject = Subject.objects.all()

    if request.GET.get('delete'):
        # Handle deletion of a class
        try:
            subject_id = request.GET.get('delete')
            subject_obj = get_object_or_404(Subject, id=subject_id)
            subject_obj.delete()
            messages.success(request, "Subject deleted successfully.")
        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            return redirect('manage_subject')
    return render(request, 'manage_subject.html', locals())


@login_required(login_url='admin_login')
def edit_subject(request, subject_id):
    subject_obj = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
      
        try:
           subject_obj.subject_name = subject_name
           subject_obj.subject_code = subject_code
        
           subject_obj.save()

           messages.success(request, "Subject updated successfully.")
           return redirect(manage_subject)
          

        except Exception as e:
            messages.error(request, f"Error updating Subject.{str(e)}")  
            return redirect(manage_subject)

    
  
    return render(request, 'edit_subject.html', locals())


@login_required(login_url='admin_login')
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
           class_id = request.POST.get('class')
           subject_id = request.POST.get('subject')

           SubjectCombination.objects.create(student_class_id=class_id, subject_id=subject_id, status=1)
           messages.success(request, "Subject combination added successfully.")

        except Exception as e:
            messages.error(request, f"Error creating Subject.{str(e)}")  
            return redirect(add_subject_combination)
    return render(request, 'add_subject_combination.html', locals())

@login_required(login_url='admin_login')
def manage_subject_combination(request):

    # Fetch all classes from database
    combinations = SubjectCombination.objects.all()

    aid = request.GET.get('aid')


    if request.GET.get('aid'):
        # Handle deletion of a class
        try:
            SubjectCombination.objects.filter(id = aid).update(status=1)
            messages.success(request, "Subject combination activated successfully.")
        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            return redirect('manage_subject_combination')
        
    did = request.GET.get('did')


    if request.GET.get('did'):
        # Handle deletion of a class
        try:
            SubjectCombination.objects.filter(id = did).update(status=0)
            messages.success(request, "Subject combination deactivated successfully.")
        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            return redirect('manage_subject_combination')
    return render(request, 'manage_subject_combination.html', locals())


@login_required(login_url='admin_login')
def add_student(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
           name = request.POST.get('fullname')
           roll_id = request.POST.get('rollID')
           email = request.POST.get('email')
           gender = request.POST.get('gender')
           dob = request.POST.get('dob')
           class_id = request.POST.get('class')
           student_class = Class.objects.get(id=class_id)
           Student.objects.create(name=name, roll_id = roll_id, email=email, gender=gender, dob=dob, student_class=student_class)
           messages.success(request, "Student info added successfully.")

        except Exception as e:
            messages.error(request, f"Error creating Subject.{str(e)}")  
            return redirect(add_student)
    return render(request, 'add_student.html', locals())


@login_required(login_url='admin_login')
def manage_student(request):

    # Fetch all classes from database
    students= Student.objects.all()

 

    return render(request, 'manage_student.html', locals())



@login_required(login_url='admin_login')
def edit_student(request, student_id):
    student_obj = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        
        try:
            student_obj.name = request.POST.get('fullname')
            student_obj.roll_id = request.POST.get('rollID')
            student_obj.email = request.POST.get('email')
            student_obj.gender = request.POST.get('gender')
            student_obj.dob= request.POST.get('dob')
            student_obj.status = request.POST.get('status')
      
           
            student_obj.save()
            messages.success(request, "Student updated successfully.")
            return redirect(manage_student)
          

        except Exception as e:
            messages.error(request, f"Error updating Student.{str(e)}")  
            return redirect(manage_student)

    
  
    return render(request, 'edit_student.html', locals())




    
@login_required(login_url='admin_login')
def add_notice(request):
    if request.method == 'POST':
        try:
           title = request.POST.get('title')
           details = request.POST.get('details')
         
           Notice.objects.create(title=title, details = details)
           messages.success(request, "Notice info added successfully.")

        except Exception as e:
            messages.error(request, f"Error creating Notice.{str(e)}")  
            return redirect(add_notice)
    return render(request, 'add_notice.html', locals())


@login_required(login_url='admin_login')
def manage_notice(request):

   
    notices = Notice.objects.all()

    if request.GET.get('delete'):
        # Handle deletion of a class
        try:
            notice_id = request.GET.get('delete')
            notice_obj = get_object_or_404(Notice, id=notice_id)
            notice_obj.delete()
            messages.success(request, "Notice deleted successfully.")
        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            return redirect('manage_notice')
    return render(request, 'manage_notice.html', locals())



@login_required(login_url='admin_login')
def add_result(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            class_id = request.POST.get('class_id')
            student_id = request.POST.get('student_id')

            # Extract test & exam marks per subject
            test_data = {
                key.split('_')[1]: value
                for key, value in request.POST.items()
                if key.startswith('test_')
            }

            exam_data = {
                key.split('_')[1]: value
                for key, value in request.POST.items()
                if key.startswith('exam_')
            }

            for subject_id in test_data:
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    test_marks=test_data.get(subject_id, 0),
                    exam_marks=exam_data.get(subject_id, 0),
                )

            messages.success(request, "Result info added successfully.")
            return redirect('add_result')

        except Exception as e:
            messages.error(request, f"Error declaring result: {str(e)}")
            return redirect('add_result')

    return render(request, 'add_result.html', locals())

from django.http import JsonResponse

def get_students_subjects(request):
    class_id = request.GET.get('class_id')

    if class_id:
        students = list(Student.objects.filter(student_class_id=class_id).values('id', 'name','roll_id'))

        subject_combinations = SubjectCombination.objects.filter(student_class_id=class_id, status=1).select_related('subject')

        #sc for SubjectCombination

        subjects = [ {'id' : sc.subject.id, 'name':sc.subject.subject_name} for sc in  subject_combinations ]

        return JsonResponse({'students': students,'subjects': subjects })

    return JsonResponse({'students': [],'subjects': []})



@login_required(login_url='admin_login')
def manage_result(request):

   
    results = Result.objects.select_related('student','student_class').all()
    students = {}
    for res in results:
        stu_id = res.student.id
        if stu_id not in students:
            students[stu_id] = {
                'student': res.student,
                'class': res.student_class,
                'reg_date': res.student.reg_date,
                'status': res.student.status,
            }

    return render(request, 'manage_result.html', {'results': students.values()})


@login_required(login_url='admin_login')
def edit_result(request, stid):
    student = get_object_or_404(Student, id=stid)
    results = Result.objects.filter(student=student)

    if request.method == 'POST':
        ids = request.POST.getlist('id[]')
        test_marks = request.POST.getlist('test_marks[]')
        exam_marks = request.POST.getlist('exam_marks[]')

        for i in range(len(ids)):
            result_obj = get_object_or_404(Result, id=ids[i])
            result_obj.test_marks = test_marks[i]
            result_obj.exam_marks = exam_marks[i]
            result_obj.save()  # recalculates total & grade

        messages.success(request, "Result updated successfully.")
        return redirect('manage_result')

    return render(request, 'edit_result.html', locals())

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='admin_login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('change_password')

        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password updated successfully.")
        return redirect('change_password')

    return render(request, 'change_password.html')



def search_result(request):
    classes = Class.objects.all()

    return render(request, 'search_result.html', locals())


def check_result(request):
    if request.method == 'POST':
        rollid = request.POST.get('rollid')
        class_id = request.POST.get('class_id')

        try:
            student = Student.objects.get(
                roll_id=rollid,
                student_class_id=class_id
            )

            results = Result.objects.filter(student=student).only('total_marks', 'status')


            total_marks = sum(r.total_marks for r in results)
            subject_count = results.count()
            max_total = subject_count * 100

            percentage = (total_marks / max_total) * 100 if max_total > 0 else 0
            percentage = round(percentage, 2)

            # Overall Pass / Fail
            overall_status = (
                "Pass" if all(r.status == "Pass" for r in results) else "Fail"
            )

            return render(request, 'result_page.html', locals())

        except Student.DoesNotExist:
            messages.error(request, "No results found for the given Roll ID and Class")
            return redirect('search_result')


@login_required(login_url='admin_login')
def admin_view_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = Result.objects.filter(student=student)

    context = {
        'student': student,
        'results': results
    }
    return render(request, 'admin_view_result.html', context)        