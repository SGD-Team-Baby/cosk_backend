# Generated by Django 4.0.6 on 2022-08-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='subtitle',
            field=models.TextField(blank=True),
        ),
    ]
