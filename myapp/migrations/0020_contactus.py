# Generated by Django 4.2.1 on 2023-08-06 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_customuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=20)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
    ]
