from django.contrib import admin
from quiz.models import *
from .models import Quiz


class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.StackedInline):
    model = Question
    inlines = [AnswerAdmin]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAdmin, AnswerAdmin]