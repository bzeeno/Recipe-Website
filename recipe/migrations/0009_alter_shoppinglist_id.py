# Generated by Django 3.2.5 on 2021-07-31 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_remove_recipe_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
