# Generated by Django 4.2.1 on 2023-06-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_remove_books_book_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='price',
        ),
        migrations.AddField(
            model_name='books',
            name='available_quantity',
            field=models.IntegerField(default=0),
        ),
    ]