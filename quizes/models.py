from django.db import models
import random
from quiz.models import *

# from quiz.models import Category
# Create your models here.
import random

DIFFICULTY_CHOICES = (
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Hard", "Hard"),
)

# Topic class
# class Topic(models.Model):
#     """Topic: The topic of the quizes
#     """

#     name = models.CharField(max_length=120)
    
#     description = models.TextField(
#         default="Programming",
#         blank=True,
#         null=True
#     )

#     date = models.DateTimeField(
#         auto_now_add=True,
#         blank=True,
#         null=True
#     )

#     def __str__(self):
#         """
#         Show the topic name in the Admin page
#         """
#         return self.name


# Quiz model
class Quiz(models.Model):
    """Quiz: The base of our app
    """

    name = models.CharField(max_length=150)

    description = models.TextField(
        default="Another quiz!",
        blank=True,
        null=True
    )

    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    # topic = models.ForeignKey(
    #     Topic,
    #     on_delete=models.SET_NULL,
    #     help_text="The topic the quiz will be evaluating about",
    #     null=True,
    #     blank=True,
    #     related_name="quizes" # The way we reference the quiz using a Topic object
    # )
    
    category = models.ForeignKey(
        'quiz.Category',  # Use string reference to avoid circular import
        on_delete=models.SET_NULL,
        help_text="The category the quiz will be about",
        null=True,
        blank=True,
        related_name="quizes"  # Updated related_name
    )

    number_of_questions = models.PositiveIntegerField(null=True)

    time = models.PositiveIntegerField(
        help_text="Duration of the quiz in minutes"
    )

    
    required_score = models.DecimalField(
        help_text="Score needed to pass the quiz in %",
        max_digits=6,
        decimal_places=2,
        # validators=PERCENTAGE_VALIDATOR
    )

    difficulty = models.CharField(
        help_text="The difficulty of the quiz",
        max_length=6,
        choices=DIFFICULTY_CHOICES
    )

    def __str__(self):
        return f"{self.name} - {self.category}"

    @property
    def get_questions(self):
        questions = list(self.questions.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = "Quizes"

