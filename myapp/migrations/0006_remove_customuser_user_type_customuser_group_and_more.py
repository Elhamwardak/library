# Generated by Django 4.2.1 on 2023-07-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_customuser_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_type',
        ),
        migrations.AddField(
            model_name='customuser',
            name='Group',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
