from django.urls import path

from . import views
urlpatterns = [
    # path('', views.index, name='quiz_index'),
    path('about/', views.about, name='quiz_about'),
    path('', views.home, name='quiz_home'),
    path('take_quiz/', views.take_quiz, name='take_quiz'),
    path('quiz/', views.quiz, name='quiz'),
    path('api/get-quiz/', views.get_quiz, name='get_quiz')
]
