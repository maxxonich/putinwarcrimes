# Generated by Django 4.1.2 on 2022-10-27 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('putinwarcrimes', '0004_remove_photo_created_remove_photo_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorydescription',
            name='language_id',
        ),
    ]