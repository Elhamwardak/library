# Generated by Django 4.2.1 on 2023-08-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone_number',
            field=models.IntegerField(max_length=16),
        ),
    ]