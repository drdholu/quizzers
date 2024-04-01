from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponse
from results.models import Result
from quiz.models import Question, Answer, Category
from .models import Quiz

from tablib import Dataset
import pandas as pd
from .forms import UploadCSVForm



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


# def save_quiz_view(request, pk):
#     if request.accepts("application/json"):
#         data = request.POST
#         data_ = dict(data.lists())
#         data_.pop('csrfmiddlewaretoken')

#         questions = []

#         for k in data_.keys():
#             question = Question.objects.get(text=k)
#             questions.append(question)

#         user = request.user
#         quiz = Quiz.objects.get(pk=pk)

#         required_score = quiz.required_score
#         score = 0
#         multiplier = 100 / len(questions) 
#         results = []

#         for q in questions:
#             a_selected = data[q.text]

#             if a_selected != '':
#                 correct_answer = Answer.objects.filter(question=q).get(correct=True)
#                 if a_selected == correct_answer.text:
#                     score += 1
                
#                 results.append({q.text: {
#                     'correct_answer': correct_answer.text,
#                     'answered': a_selected
#                 }})
#             else:
#                 results.append({q.text: 'not answered'})

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


def save_quiz_view(request, pk):
    if request.accepts("application/json"):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        questions = []

        for k in data_.keys():
            # Since 'k' represents the question text, we need to filter questions by 'question' field
            question = Question.objects.get(question=k)  # Adjusted to match the 'question' field
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        required_score = quiz.required_score
        score = 0
        multiplier = 100 / len(questions)
        results = []

        for q in questions:
            # Adjusted to match the 'question' field
            a_selected = data[q.question] if q.question in data else ''

            if a_selected != '':
                # Filter answers by 'answer' field
                correct_answer = Answer.objects.filter(question=q, is_correct=True).first()
                if correct_answer and a_selected == correct_answer.answer:
                    score += 1

                results.append({q.question: {
                    'correct_answer': correct_answer.answer if correct_answer else '',  # Adjusted to match the 'answer' field
                    'answered': a_selected
                }})
            else:
                results.append({q.question: 'not answered'})

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

# views.py

# def upload_quiz(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         # file_path = csv_file.temporary_name()
#         csv_data = io.BytesIO(csv_file.read())
#         # Process the CSV file
#         process_csv_file(csv_data)
#         return render(request, 'quizes/success.html')
#     return render(request, 'quizes/upload_quiz.html')

# def upload_quiz(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         csv_data = csv_file.read().decode('utf-8')  # Read content as text

#         try:
#             process_csv_file(csv_data)  # Pass the data directly
#             return render(request, 'quizes/success.html')
#         except Exception as e:
#             # Handle any errors
#             return HttpResponse(f'<h1>Error {e}</h1>')

#     return render(request, 'quizes/upload_quiz.html')



# def process_csv_file(csv_file):
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         # Create or get category
#         category, created = Category.objects.get_or_create(category_name=row['Category'])
#         # Create or get quiz
#         quiz, created = Quiz.objects.get_or_create(
#             name=row['Quiz'],
#             category=category,
#             time=row['Time'],
#             required_score=row['Required Score'],
#             difficulty=row['Difficulty']
#         )
#         # Create question
#         question = Question.objects.create(
#             quiz=quiz,
#             question=row['Question'],
#             marks=row['Marks']
#         )
#         # Create answer
#         answer = Answer.objects.create(
#             question=question,
#             answer=row['Answer'],
#             is_correct=True if row['Is Correct'] == 'True' else False
#         )

def upload_quiz(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            process_csv_file(csv_file)
            return render(request, 'success.html')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_quiz.html', {'form': form})

def process_csv_file(csv_file):
    dataset = Dataset()
    imported_data = dataset.load(csv_file.read().decode('utf-8'), format='csv')
    for data in imported_data:
        category, created = Category.objects.get_or_create(category_name=data['Category'])
        quiz, created = Quiz.objects.get_or_create(
            name=data['Quiz'],
            category=category,
            time=data['Time'],
            required_score=data['Required Score'],
            number_of_questions=data['Number of Questions'],
            difficulty=data['Difficulty']
        )
        question = Question.objects.create(quiz=quiz, question_text=data['Question'])
        answer = Answer.objects.create(question=question, answer_text=data['Answer'], is_correct=data['Is Correct'])

# def upload_quiz(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         # Process the CSV file
#         process_csv_file(csv_file)
#         return render(request, 'quizes/success.html')
#     return render(request, 'quizes/upload_quiz.html')

# def process_csv_file(csv_file):
#     csv_data = csv_file.read().decode('utf-8')
#     reader = csv.DictReader(StringIO(csv_data))
    
#     for row in reader:
#         # print(row.keys())
#         # Create or get category
#         category, created = Category.objects.get_or_create(category_name=row['category_name'])
#         # Create or get quiz
#         quiz, created = Quiz.objects.get_or_create(
#             name=row['quiz_name'],
#             category=category,
#             time=row['time'],
#             required_score=row['required_score'],
#             difficulty=row['difficulty']
#         )
#         # Create question
#         question = Question.objects.create(
#             quiz=quiz,
#             question=row['question_text'],
#             marks=row['marks']
#         )
#         # Create answer
#         answer = Answer.objects.create(
#             question=question,
#             answer=row['answer_text'],
#             is_correct=True if row['is_correct'] == 'True' else False
#         )


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
