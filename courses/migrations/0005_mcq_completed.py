# Generated by Django 3.2.7 on 2021-10-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('courses', '0004_mcq_mcqtranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcq',
            name='completed',
            field=models.ManyToManyField(related_name='completed_mcqs', to='users.Profile'),
        ),
    ]
