from django.shortcuts import render, redirect
from .models import *
from quizes.models import *
from django.http import HttpResponse, JsonResponse
import random

# Quiz API - Shuffles questions
def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        data = []
        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        
        question_objs = list(question_objs)
        
        random.shuffle(question_objs) #allows us to select random questions
        for question_obj in question_objs:
            data.append({
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                # instead of bringing answers data here, we make a function in Question model itself and call it here
                'answers': question_obj.get_ans()
            })
            
        payload = {'status': True, 'data': data}
        return JsonResponse(payload)
        
    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")

def take_quiz(request):
    context = {'categories': Category.objects.all(), 
               'questions': Question.objects.all(),
               'quizes': Quiz.objects.all()}
    
    # if request.GET.get('category'):
    #     return redirect(f"/quiz/?category={request.GET.get('category')}")
    
    return render(request, 'take_quiz.html', context)

def quiz(request):
    return render(request, 'quiz.html')


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')