# Generated by Django 4.2.1 on 2023-08-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_books_book_descriptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='file',
        ),
        migrations.AddField(
            model_name='books',
            name='book_file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
