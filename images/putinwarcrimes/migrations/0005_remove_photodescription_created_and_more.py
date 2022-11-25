# Generated by Django 4.1.2 on 2022-11-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('putinwarcrimes', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photodescription',
            name='created',
        ),
        migrations.RemoveField(
            model_name='photodescription',
            name='updated',
        ),
        migrations.AddField(
            model_name='photo',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
