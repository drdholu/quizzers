from django.contrib import admin
from quiz.models import *
from .models import Quiz

# Register your models here.
class AnswerAdmin(admin.TabularInline):
    model = Answer
    extra = 0
    
    
class QuestionAdmin(admin.StackedInline):
    model = Question
    inlines = [AnswerAdmin]

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAdmin]


admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Topic)