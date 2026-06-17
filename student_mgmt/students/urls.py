from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    # Student CRUD URLs
    path('',views.student_list,name='student_list'),
    path('add/', views.student_create, name='student_create'),
    path('edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),

    # Student details+marks
    path('<int:pk>/',views.student_detail,name='student_detail'),
    path('<int:pk>/add-mark/',views.add_mark,name='add_mark'),

    # Mark edit/delete (uses the Mark's own pk, not the student's)
    path('mark/<int:pk>/edit/',   views.edit_mark,   name='edit_mark'),
    path('mark/<int:pk>/delete/', views.delete_mark, name='delete_mark')
]