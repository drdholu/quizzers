from django.urls import path

# from .views import (
#     QuizListView,
#     QuizDetailView,
#     # quiz_detail_data_view,
#     # save_quiz_view
# )
from . import views

app_name = 'quizes'

urlpatterns = [
    # path('take_quiz/test', QuizListView.as_view(), name='quiz_list_view'),
    path('quiz_list/', views.QuizListView.as_view(), name='quiz_list_view'),
    path('quiz_list/quiz/<pk>', views.QuizDetailView.as_view(), name='quiz_view'),
    path('quiz_list/quiz/<pk>/data',views.quiz_detail_data_view, name='quiz_data_view'),
    path('quiz_list/quiz/<pk>/save', views.save_quiz_view, name='quiz_save_view'),
]
