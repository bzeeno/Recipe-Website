# Generated by Django 3.2.5 on 2021-08-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_auto_20210801_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
