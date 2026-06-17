# Student Management System

A full-stack web application built with Django for managing student records, grades, and academic performance — featuring role-based authentication, CRUD operations, search and filtering, and a personalized grade report system.

## Features

- **Student records management** — create, view, edit, and delete student profiles (name, roll number, email, class)
- **Marks and grading** — record exam scores per subject, with automatic letter grade calculation and average score reporting
- **Role-based access control** — three distinct access levels:
  - **Admin** (`is_staff=True`) — full access to add, edit, and delete students and marks
  - **Viewer** — read-only access to the full student list and grade reports
  - **Student** — linked to their own record via a one-to-one relationship, can only view their own grade report
- **Authentication** — custom login and logout flow built on Django's built-in auth system, with session-based access control
- **Search and filtering** — search students by name or roll number, filter by class, powered by Django ORM `Q` objects
- **Pagination** — student list is paginated for better performance and usability
- **Django Admin integration** — all models are registered in the admin panel for quick data management

## Tech stack

- **Backend:** Python, Django 6.0
- **Database:** SQLite (development)
- **Frontend:** Django Templates, Bootstrap 5
- **Auth:** Django's built-in authentication system (`django.contrib.auth`)

## Project structure

```
student_mgmt/
├── student_mgmt/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── students/               # Main application
│   ├── templates/
│   │   └── students/
│   │       ├── student_list.html
│   │       ├── student_form.html
│   │       ├── student_confirm_delete.html
│   │       ├── student_detail.html
│   │       ├── mark_form.html
│   │       ├── mark_confirm_delete.html
│   │       └── login.html
│   ├── models.py           # Student and Mark models
│   ├── forms.py            # ModelForms for Student and Mark
│   ├── views.py            # All application views
│   ├── urls.py              # App-level URL routing
│   └── admin.py             # Django admin registration
└── manage.py
```

## Data models

**Student**
| Field | Type | Notes |
|---|---|---|
| user | OneToOneField (User) | Optional link to a Django User account |
| name | CharField | Full name |
| roll_no | CharField | Unique roll number |
| email | EmailField | Unique email address |
| class_name | CharField | Class or section |
| created_at | DateTimeField | Auto-set on creation |

**Mark**
| Field | Type | Notes |
|---|---|---|
| student | ForeignKey (Student) | One student can have many marks |
| subject | CharField | Subject name |
| score | DecimalField | Score out of 100 |
| exam_date | DateField | Date of the exam |

The `Mark` model includes a `get_grade()` method that converts a numeric score into a letter grade (A+, A, B, C, D, F).

## Setup and installation

1. Clone the repository and navigate into the project folder

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1      # Windows PowerShell
   ```

3. Install dependencies
   ```bash
   pip install django
   ```

4. Apply database migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create an admin account
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

7. Visit the app
   - Student list: `http://127.0.0.1:8000/students/`
   - Login page: `http://127.0.0.1:8000/students/login/`
   - Django admin: `http://127.0.0.1:8000/admin/`

## User roles

| Role | How to create | Access level |
|---|---|---|
| Admin | `python manage.py createsuperuser` | Full CRUD on students and marks |
| Viewer | `User.objects.create_user(username, password)` | Read-only access to all student records |
| Student | Create a User, then link it via `student.user = user` | Can only view their own grade report |

## Key Django concepts demonstrated

- Models, migrations, and the Django ORM (`ForeignKey`, `OneToOneField`, `related_name`)
- ModelForms with custom widgets and validation
- Class-based filtering with `Q` objects (`icontains`, OR/AND logic)
- Aggregation queries (`Avg`) for calculating average scores
- Pagination with `Paginator`
- Authentication and session management (`authenticate`, `login`, `logout`)
- View-level permission checks (`@login_required`, `is_staff`, custom ownership checks)
- Django's messages framework for user feedback
- CSRF protection on all POST forms

## Roadmap

- [ ] CSV and PDF export of student data and grade reports
- [ ] Profile picture upload (`ImageField` + media file handling)
- [ ] Custom 404 / 500 error pages
- [ ] Deployment to Railway or Render with PostgreSQL
- [ ] Environment-based configuration with `python-decouple`

## License

This project was built as a learning exercise and portfolio piece. Free to use and adapt.
