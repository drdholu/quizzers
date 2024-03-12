from django.db import models
import uuid

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