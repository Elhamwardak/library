# Generated by Django 4.2.1 on 2023-06-08 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_books_cover_photo_issuebook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuebook',
            name='username',
        ),
    ]