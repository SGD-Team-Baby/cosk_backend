# Generated by Django 4.0.6 on 2022-08-17 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
