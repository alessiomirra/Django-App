# Generated by Django 4.1.7 on 2023-04-01 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_rename_file_image_image_delete_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='image',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
