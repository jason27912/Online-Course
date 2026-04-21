from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/submit/', views.submit_exam, name='submit_exam'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_results, name='show_exam_results'),
]
