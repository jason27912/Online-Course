from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
    show_change_link = True

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'lesson', 'points']
    list_filter = ['lesson__course']
    search_fields = ['text']
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']
    inlines = [QuestionInline]

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'selected_choice', 'is_correct', 'submitted_at']
    list_filter = ['is_correct', 'question__lesson__course']
    search_fields = ['user__username']

admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
