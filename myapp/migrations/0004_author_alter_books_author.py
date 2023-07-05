# Generated by Django 4.2.1 on 2023-07-04 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_books_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.author'),
        ),
    ]