from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Question, Choice, Submission

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course/course_details_bootstrap.html', {'course': course})

@login_required
def take_exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    return render(request, 'course/take_exam.html', {'lesson': lesson, 'questions': questions})

@login_required
def submit_exam(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    score = 0
    total_points = 0
    selected_ids = []
    
    for question in questions:
        total_points += question.points
        selected_choice_id = request.POST.get(f'question_{question.id}')
        
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            selected_ids.append(selected_choice_id)
            is_correct = selected_choice.is_correct
            
            Submission.objects.create(
                user=request.user,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )
            
            if is_correct:
                score += question.points
    
    grade = (score / total_points * 100) if total_points > 0 else 0
    
    return render(request, 'course/exam_result_bootstrap.html', {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': total_points,
    })

def show_exam_results(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submissions = Submission.objects.filter(id=submission_id, user=request.user)
    selected_ids = [str(sub.selected_choice.id) for sub in submissions]
    
    total_score = 0
    possible_score = 0
    
    for sub in submissions:
        possible_score += sub.question.points
        if sub.is_correct:
            total_score += sub.question.points
    
    grade = (total_score / possible_score * 100) if possible_score > 0 else 0
    
    return render(request, 'course/exam_result_bootstrap.html', {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': possible_score,
    })
