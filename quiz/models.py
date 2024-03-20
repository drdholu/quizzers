from django.db import models
import uuid
import random

# Create your models here.

# Base model to reduce repeatition of code.
class BaseModel(models.Model):
   uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   created_at = models.DateField(auto_now_add=True) 
   updated_at = models.DateField(auto_now=True)
   
   # While migration, we don't want to register this model as a table in our DB, we want to use this as a Class.
   class Meta:
       abstract = True  # this register BaseModel as a base class.
   
class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
    

# related_name allows to have a reverse relationship between models
class Question(BaseModel):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)
    
    def __str__(self):
        return self.question
    
    def get_ans(self):
        # this creates a list of the answers
        answer_objs = list(Answer.objects.filter(question=self)) # converted into a list to allow shuffling
        random.shuffle(answer_objs)
        data = []
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data
    
    

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer
    
    
    
# make sure to register the models in admin.py

'''
1. Add a category
2. Add questions
3. Add Answer to that question
'''