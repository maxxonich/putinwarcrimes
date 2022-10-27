# Generated by Django 4.1.2 on 2022-10-26 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('putinwarcrimes', '0003_photo_created_photo_size_photo_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='created',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='size',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='updated',
        ),
        migrations.AddField(
            model_name='photodescription',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='photodescription',
            name='size',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='photodescription',
            name='updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]