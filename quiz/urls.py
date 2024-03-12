from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name='quiz_index'),
    path('about/', views.about, name='quiz_about'),
    path('', views.home, name='quiz_home'),
]
