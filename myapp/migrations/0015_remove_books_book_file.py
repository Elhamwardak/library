# Generated by Django 4.2.1 on 2023-06-12 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_books_issue_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='book_file',
        ),
    ]
