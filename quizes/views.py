from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from results.models import Result
from quiz.models import Question, Answer
from .models import Quiz



# Quiz List view
class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    # return render(request, 'quizes/main.html', context)
    

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quizes/detail.html'

# def quiz_detail_data_view(request, pk):
#     quiz = Quiz.objects.get(pk=pk)
#     questions = []
#     for question in quiz.get_questions:
#         answers = []
#         for answer in question.get_answers:
#             answers.append(answer.text)
#         questions.append({question.text: answers})
    
#     return JsonResponse({
#         'data': questions,
#         'time': quiz.time
#     })
    

def quiz_detail_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []

    for question in quiz.get_questions:
        answers = []
        for answer in question.question_answer.all():  # Access related Answer objects using 'question_answer'
            answers.append(answer.answer)
        questions.append({question.question: answers})
    
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


def save_quiz_view(request, pk):
    if request.accepts("application/json"):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        questions = []

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(questions) 
        results = []

        for q in questions:
            a_selected = data[q.text]

            if a_selected != '':
                correct_answer = Answer.objects.filter(question=q).get(correct=True)
                if a_selected == correct_answer.text:
                    score += 1
                
                results.append({q.text: {
                    'correct_answer': correct_answer.text,
                    'answered': a_selected
                }})
            else:
                results.append({q.text: 'not answered'})

        final_score = score * multiplier


        Result.objects.create(quiz=quiz, user=user, score=final_score)

        json_response = {
            'score': final_score,
            'correct_questions': score,
            'passed': False,
            'required_score': required_score,
            'results': results
        }

        if final_score >= required_score:
            json_response['passed'] = True
            return JsonResponse(json_response)    

        return JsonResponse(json_response)

# from django.shortcuts import render, redirect
# from django.views.generic import ListView, DetailView
# from django.http import JsonResponse
# from results.models import Result
# from quiz.models import Quiz, Question, Answer


# # Quiz List view
# class QuizListView(ListView):
#     model = Quiz
#     template_name = 'quizes/main.html'


# class QuizDetailView(DetailView):
#     model = Quiz
#     template_name = 'quizes/detail.html'


# def quiz_detail_data_view(request, pk):
#     quiz = Quiz.objects.get(pk=pk)
#     questions = []
#     for question in quiz.get_questions:
#         answers = []
#         for answer in question.get_ans():  # Updated method call
#             answers.append(answer['answer'])  # Updated dictionary access
#         questions.append({question.question: answers})  # Updated attribute access
    
#     return JsonResponse({
#         'data': questions,
#         'time': quiz.time
#     })


# def save_quiz_view(request, pk):
#     if request.accepts("application/json"):
#         data = request.POST
#         data_ = dict(data.lists())
#         data_.pop('csrfmiddlewaretoken')

#         questions = []

#         for k in data_.keys():
#             question = Question.objects.get(question=k)  # Updated attribute access
#             questions.append(question)

#         user = request.user
#         quiz = Quiz.objects.get(pk=pk)

#         required_score = quiz.required_score
#         score = 0
#         multiplier = 100 / len(questions)
#         results = []

#         for q in questions:
#             a_selected = data[q.question]  # Updated attribute access

#             if a_selected != '':
#                 correct_answer = Answer.objects.filter(question=q).get(is_correct=True)  # Updated attribute access
#                 if a_selected == correct_answer.answer:  # Updated attribute access
#                     score += 1

#                 results.append({q.question: {
#                     'correct_answer': correct_answer.answer,  # Updated attribute access
#                     'answered': a_selected
#                 }})
#             else:
#                 results.append({q.question: 'not answered'})  # Updated attribute access

#         final_score = score * multiplier

#         Result.objects.create(quiz=quiz, user=user, score=final_score)

#         json_response = {
#             'score': final_score,
#             'correct_questions': score,
#             'passed': False,
#             'required_score': required_score,
#             'results': results
#         }

#         if final_score >= required_score:
#             json_response['passed'] = True
#             return JsonResponse(json_response)

#         return JsonResponse(json_response)
