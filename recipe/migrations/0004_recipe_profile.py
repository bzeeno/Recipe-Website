# Generated by Django 3.2.5 on 2021-07-25 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('recipe', '0003_auto_20210724_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='profile',
            field=models.ManyToManyField(to='users.Profile'),
        ),
    ]
