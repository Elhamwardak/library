# Generated by Django 4.2.1 on 2023-07-13 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_customuser_created_at_customuser_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_id',
        ),
    ]