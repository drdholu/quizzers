# Python Queries

## Fetch questions and answers using related name

> 'django_extensions' is used to import everything

```python
>>> category = Category.objects.all()                  
>>> category
<QuerySet [<Category: Django>]>
>>> category[0].category.all()
<QuerySet [<Question: What is Django?>, <Question: Which Language does Django use?>]>
>>> category[0].category.first()
<Question: Which Language does Django use?>
>>> category[0].category.first().question_answer.all()
<QuerySet [<Answer: Python>, <Answer: C++>, <Answer: Javascript>]>
>>> exit()
```