# Generated by Django 4.2.1 on 2023-11-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_alter_contactus_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
    ]