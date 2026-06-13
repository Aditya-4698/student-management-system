from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Student,Book,IssueBook
from .forms import BookForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.pagesizes import A4
import os
from django.conf import settings
from django.contrib.auth.models import User




def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'students/signup.html')



def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect('index')

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, 'students/login.html')




def logout(request):

    auth_logout(request)

    messages.success(
        request,
        "Logged Out Successfully"
    )

    return redirect('login')











# Create your views here.
def home(request):
    return render(request,'students/home.html')


@login_required
def add_student(request):
    if request.method == 'POST':


        Student.objects.create(

            # Student Details
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            dob=request.POST.get('dob') or None,
            gender=request.POST.get('gender'),
            course=request.POST.get('course'),
            roll_no=request.POST.get('roll_no'),

            # Parent Details
            father_name=request.POST.get('father_name'),
            mother_name=request.POST.get('mother_name'),
            parent_contact=request.POST.get('parent_contact'),
            occupation=request.POST.get('occupation'),

            # Address Details
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),

            # Academic Details
            obtained_marks=request.POST.get('obtained_marks') or 0,
            total_marks=request.POST.get('total_marks') or 0,

            # Image
            image=request.FILES.get('image')
        )
        messages.success(request, "Student Registered Successfully!")
        return redirect('index')

    return render(request,'students/add_student.html')




@login_required
def view_students(request):

    search = request.GET.get('search')

    students = Student.objects.all().order_by('id')

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(roll_no__icontains=search) |
            Q(course__icontains=search)
        )

    return render(
        request,
        'students/view_students.html',
        {
            'students': students
        }
    )
            

@login_required
def update_student(request,id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.dob = request.POST.get('dob')
        student.gender = request.POST.get('gender')
        student.course = request.POST.get('course')
        student.roll_no = request.POST.get('roll_no')


        student.father_name = request.POST.get('father_name')
        student.mother_name = request.POST.get('mother_name')
        student.parent_contact = request.POST.get('parent_contact')
        student.occupation = request.POST.get('occupation')


        student.address = request.POST.get('address')
        student.city = request.POST.get('city')
        student.state = request.POST.get('state')
        student.pincode = request.POST.get('pincode')

        student.obtained_marks = request.POST.get('obtained_marks') or 0
        student.total_marks = request.POST.get('total_marks') or 0

        if request.FILES.get('image'):
            student.image = request.FILES.get('image')

        student.save()

        return redirect('view_students')
    
    return render(request,'students/update_student.html', {'student': student}
    )    


@login_required
def delete_student(request,id):
    student = get_object_or_404(Student, id=id)

    student.delete()

    messages.success(request,"Student Record Deleted Successfully!")

    return redirect('view_students')



@login_required
def index(request):

    students = Student.objects.all().order_by('-id')[:5]

    # 📚 LIBRARY DATA
    books = Book.objects.all()

    total_books = books.count()
    issued_books = IssueBook.objects.filter(status='Issued').count()

    overdue_books = sum(
        1 for i in IssueBook.objects.filter(status='Issued')
        if i.is_overdue()
    )

    # 💰 TOTAL FINE CALCULATION
    total_fine = sum(
        i.fine_amount()
        for i in IssueBook.objects.filter(status='Issued')
    )

    # 📖 RECENT ISSUED BOOKS
    recent_issues = IssueBook.objects.filter(status='Issued').order_by('-issue_date')[:5]

    context = {
        # student
        'total_students': Student.objects.count(),
        'total_courses': Student.objects.values('course').distinct().count(),
        'toppers': Student.objects.filter(obtained_marks__gte=80).count(),
        'active_students': Student.objects.count(),
        'students': students,

        # library
        'total_books': total_books,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'total_fine': total_fine,
        'recent_issues': recent_issues,
    }

    return render(request, 'students/index.html', context)


from students.models import IssueBook

def global_context(request):

    if request.user.is_authenticated:

        issues = IssueBook.objects.filter(status='Issued')

        overdue_issues = [i for i in issues if i.is_overdue()]

        return {
            'overdue_count': len(overdue_issues),
            'overdue_issues': overdue_issues[:5],  # only top 5
        }

    return {}



def add_background(canvas, doc):

    logo_path = os.path.join(
        settings.BASE_DIR,
        "students",
        "static",
        "students",
        "images",
        "logo.png"
    )

    if os.path.exists(logo_path):

        canvas.saveState()

        try:

            canvas.setFillAlpha(0.08)

        except:
            pass

        canvas.drawImage(
            logo_path,
            150,
            250,
            width=280,
            height=280,
            mask='auto'
        )

        canvas.restoreState()


def student_report(request, id):

    student = get_object_or_404(Student, id=id)

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="{student.name}_report.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==========================
    # CUSTOM STYLES
    # ==========================

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor("#0d47a1"),
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=1,
        textColor=colors.grey
    )

    # ==========================
    # HEADER
    # ==========================

    header_data = []

    logo_path = os.path.join(
        settings.BASE_DIR,
        "students",
        "static",
        "students",
        "images",
        "logo.png"
    )

    logo = ""

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=70,
            height=70
        )

    header_data.append([
        logo,
        Paragraph(
            """
            <font size='22' color='#0d47a1'>
            <b>Innovative Learning Academy</b>
            </font><br/>
            <font size='11'>
            Official Academic Report Card
            </font>
            """,
            styles['BodyText']
        )
    ])

    header_table = Table(
        header_data,
        colWidths=[90, 380]
    )

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 20))



    # ==========================
    # STUDENT PHOTO
    # ==========================

    photo = ""

    if student.image:

        try:

            photo = Image(
                student.image.path,
                width=120,
                height=120
            )

        except:
            photo = ""

    # ==========================
    # STUDENT INFO CARD
    # ==========================

    info_table = Table(
        [[

            Paragraph(
                f"""
                <b>Name:</b> {student.name}<br/>
                <b>Roll No:</b> {student.roll_no}<br/>
                <b>Course:</b> {student.course}<br/>
                <b>Email:</b> {student.email}<br/>
                <b>Phone:</b> {student.phone}
                """,
                styles['BodyText']
            ),

            photo

        ]],
        colWidths=[350, 120]
    )

    info_table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')

    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 20))

    # ==========================
    # STUDENT DETAILS TABLE
    # ==========================

    data = [

        ["Field", "Details"],

        ["Date Of Birth", str(student.dob)],
        ["Gender", student.gender],
        ["Father Name", student.father_name],
        ["Mother Name", student.mother_name],
        ["Parent Contact", student.parent_contact],
        ["Occupation", student.occupation],
        ["Address", student.address],
        ["City", student.city],
        ["State", student.state],
        ["Pincode", student.pincode],

    ]

    table = Table(
        data,
        colWidths=[180, 280]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),

        ('GRID', (0, 0), (-1, -1), 1, colors.grey),

        ('ROWBACKGROUNDS',
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.lightgrey])

    ]))

    elements.append(table)

    elements.append(Spacer(1, 10))

    # ==========================
    # RESULT CALCULATION
    # ==========================

    percentage = 0

    if student.total_marks and student.total_marks > 0:

        percentage = (
            student.obtained_marks * 100
        ) / student.total_marks

    if percentage >= 90:
        grade = "A+"

    elif percentage >= 80:
        grade = "A"

    elif percentage >= 70:
        grade = "B"

    elif percentage >= 60:
        grade = "C"

    else:
        grade = "D"

    # ==========================
    # RESULT SECTION
    # ==========================

    elements.append(
        Paragraph(
            "📊 Academic Performance",
            styles['Heading2']
        )
    )

    result_data = [

        ["Obtained Marks", str(student.obtained_marks)],
        ["Total Marks", str(student.total_marks)],
        ["Percentage", f"{percentage:.2f}%"],
        ["Grade", grade]

    ]

    result_table = Table(
        result_data,
        colWidths=[220, 220]
    )

    result_table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#198754')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME',
        (0, 0),
        (-1, -1),
        'Helvetica-Bold'),

        ('ALIGN',
        (0, 0),
        (-1, -1),
        'CENTER'),

        ('ROWBACKGROUNDS',
        (0, 0),
        (-1, -1),
        [colors.whitesmoke, colors.lightgrey])

    ]))

    elements.append(result_table)

    elements.append(Spacer(1, 10))

    # ==========================
    # SIGNATURE
    # ==========================

    sign_path = os.path.join(
    settings.BASE_DIR,
    "students",
    "static",
    "students",
    "images",
    "signature.png"
)

    elements.append(Spacer(1, 20))

    if os.path.exists(sign_path):

        sign_img = Image(
        sign_path,
        width=140,
        height=60
    )

    sign_table = Table(
        [["", sign_img]],
        colWidths=[320, 150]
    )

    sign_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT')
    ]))

    elements.append(sign_table)

    elements.append(
        Paragraph(
            """
            <para alignment='right'>
            <b>Aditya Raj</b><br/>
            Director<br/>
            Innovative Learning Academy
            </para>
            """,
            styles['Normal']
        )
    )

    elements.append(Spacer(1, 20))

    # ==========================
    # FOOTER
    # ==========================

    footer_table = Table(
        [[
            f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            "Student Management System"
        ]],
        colWidths=[250, 220]
    )

    footer_table.setStyle(TableStyle([

        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Oblique'),

        ('TEXTCOLOR', (0,0), (-1,-1), colors.grey),

        ('ALIGN', (1,0), (1,0), 'RIGHT')

    ]))

    elements.append(Spacer(1, 10))
    elements.append(footer_table)

    # ==========================
    # BUILD PDF
    # ==========================

    doc.build(
        elements,
        onFirstPage=add_background,
        onLaterPages=add_background
    )

    return response














def book_list(request):

    books = Book.objects.all()
    issues = IssueBook.objects.filter(status='Issued')

    return render(request, 'students/book_list.html', {
        'books': books,
        'issues': issues
    })


@login_required
def add_book(request):

    if request.method == 'POST':

        form = BookForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Book Added Successfully'
            )

            return redirect('book_list')

    else:

        form = BookForm()

    return render(
        request,
        'students/add_book.html',
        {
            'form': form
        }
    )



@login_required
def issue_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    students = Student.objects.all()

    if request.method == 'POST':

        student_id = request.POST.get('student')
        return_date = request.POST.get('return_date')

        student = get_object_or_404(Student, id=student_id)

        # 🔴 check availability
        if book.available_quantity <= 0:
            messages.error(request, "Book not available")
            return redirect('book_list')

        # 🔴 check already issued
        already = IssueBook.objects.filter(
            student=student,
            book=book,
            status='Issued'
        ).exists()

        if already:
            messages.error(request, "Student already issued this book")
            return redirect('book_list')

        # ✅ create issue record
        IssueBook.objects.create(
            student=student,
            book=book,
            return_date=return_date
        )

        # ✅ reduce stock
        book.available_quantity -= 1
        book.save()

        messages.success(request, "Book Issued Successfully")
        return redirect('book_list')

    return render(request, 'students/issue_book.html', {
        'book': book,
        'students': students
    })

@login_required
def issued_books_list(request):

    issues = IssueBook.objects.filter(status='Issued').order_by('-issue_date')

    return render(request, 'students/issued_books.html', {
        'issues': issues
    })


@login_required
def return_book(request, issue_id):

    issue = get_object_or_404(IssueBook, id=issue_id)

    if issue.status == "Returned":
        messages.error(request, "Already returned")
        return redirect('book_list')

    issue.status = "Returned"
    issue.save()

    # increase stock
    issue.book.available_quantity += 1
    issue.book.save()

    messages.success(request, "Book Returned Successfully")
    return redirect('book_list')