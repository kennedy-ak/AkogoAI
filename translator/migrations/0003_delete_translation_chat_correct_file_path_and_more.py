# Generated by Django 5.0.7 on 2024-08-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0002_translation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Translation',
        ),
        migrations.AddField(
            model_name='chat',
            name='correct_file_path',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='incorrect_file_path',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='is_correct',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
