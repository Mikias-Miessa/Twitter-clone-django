# Generated by Django 3.2.18 on 2023-04-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Twitter', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='body',
            field=models.CharField(max_length=2000),
        ),
    ]
