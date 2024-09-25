# Generated by Django 4.2.1 on 2024-09-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_customuser_student_customuser_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]