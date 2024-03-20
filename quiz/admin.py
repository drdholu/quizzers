from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)

class AnswerAdmin(admin.StackedInline):
    model = Answer


# Allows us to see the answers with the Questions models
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin] # This gives no error as the Answer model has a ForeignKey with Question passed as a parameter

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)