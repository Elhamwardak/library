# Generated by Django 4.2.1 on 2023-07-19 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_group_customuser_group_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='group_id',
            new_name='group',
        ),
    ]
