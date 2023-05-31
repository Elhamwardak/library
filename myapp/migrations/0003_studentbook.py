# Generated by Django 4.2.1 on 2023-05-13 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('is_favourite', models.BooleanField(default=False)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.books')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
