# Generated by Django 4.1.2 on 2022-10-24 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('putinwarcrimes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='Photo',
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name_plural': 'Photos'},
        ),
        migrations.AddField(
            model_name='category',
            name='language',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='putinwarcrimes.language'),
            preserve_default=False,
        ),
    ]
