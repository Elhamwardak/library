# Generated by Django 4.2.1 on 2023-08-04 19:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_books_isbn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=16),
            preserve_default=False,
        ),
    ]
