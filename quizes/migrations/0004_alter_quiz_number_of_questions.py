# Generated by Django 5.0.3 on 2024-04-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0003_remove_quiz_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='number_of_questions',
            field=models.IntegerField(null=True),
        ),
    ]